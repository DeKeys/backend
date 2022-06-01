from fastapi import APIRouter, Response, status
from hashlib import sha512
import sqlalchemy
import requests
import json
import time
from datetime import datetime
from functools import wraps

from models.user import UserModel
from models.password import Password
from models.password_delete import PasswordDelete
from models.password_edit import PasswordEdit
from models.error_types import ErrorTypes

from data import db_session
from data.users import User
from data.passwords import Password as DataPassword

from constants import IPFS_URL

from routers.auth import verify_signature


router = APIRouter(prefix="/api")


def verify_user(func):
    """User verification wrapper."""

    @wraps(func)
    def verify(*args, **kwargs):
        """User verification function.

        Creates new session. Then checks that user if valid by data in BD.
        """

        session = db_session.create_session()
        model, response = kwargs.values()

        if verification_check := verify_signature(model) or\
            (user := session.query(User).where(User.public_key == model.public_key).first()) is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return verification_check or ErrorTypes.ACCOUNT_NOT_EXISTS
        
        func.__globals__["session"] = session
        func.__globals__["user"] = user

        return func(model, response)

    return verify
        

@router.post("/create_password", status_code=status.HTTP_200_OK)
@verify_user
def create_password(password: Password, response: Response):
    """Password creation function.
    
    Creates data dictionary with new password. Add this new password to IPFS.
    Get info of that data in IPFS and fill the DB with this data.

    @param password: instance of a new password
    @param response: some response
    """

    data = {
        "service": password.service,
        "login": password.login,
        "password": password.password
    }

    resp = requests.post(f"{IPFS_URL}/api/v0/add", files={
        sha512((password.service + password.login + password.password + password.public_key).encode("utf-8")).hexdigest(): json.dumps(data)
    })

    if resp.status_code != 200:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorTypes.FAILED_ADD_PASSWORD_TO_IPFS
        
    addr = resp.json()["Hash"]

    pwd = DataPassword()
    pwd.user_id = user.id
    pwd.address = addr
    pwd.created_at = datetime.now()
    session.add(pwd)
    session.commit()

    session.close()

    return addr


@router.post("/delete_password", status_code=status.HTTP_200_OK)
@verify_user
def delete_password(password: PasswordDelete, response: Response):
    """Password deletion function.
    
    Get password from DB by user id and address of a password and check if password exist in DB.
    Then simply delete password from DB.

    @param password: instance of a password that needs to be deleted
    @param response: some response
    """

    users_password = session.query(DataPassword).where(
        sqlalchemy.and_(
            DataPassword.user_id == user.id, 
            DataPassword.address == password.address
        )
    ).first()

    if not users_password:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.PASSWORD_NOT_EXIST

    session.delete(users_password)
    session.commit()

    session.close()


@router.get("/get_passwords", status_code=status.HTTP_200_OK)
@verify_user
def get_passwords(model: UserModel, response: Response):
    """Password fetching function.

    Fetch password from DB and reciece it's data from IPFS.

    @param model: instance of a user
    @param response: some response
    """

    db_passwords = session.query(DataPassword).where(DataPassword.user_id == user.id).order_by(DataPassword.created_at.desc()).all()

    passwords = []

    for db_pwd in db_passwords:
        response = requests.post(f"{IPFS_URL}/api/v0/cat/" + db_pwd.address)
        if response.status_code == 200:
            data = response.json()
            data["created_at"] = db_pwd.created_at.timestamp()
            data["address"] = db_pwd.address
            passwords.append(data)

    session.close()

    return json.dumps({
        "passwords": passwords 
    })


@router.post("/edit_password", status_code=status.HTTP_200_OK)
@verify_user
def edit_password(password: PasswordEdit, response: Response):
    """Password editing function.
    
    Fetch passowrd's information from DB and check that it exists.
    Then create dictionary with data of a new version of a password.
    After that upload password to IPFS. Using data we got from uploading on IPFS,
    update information in DB.

    @param password: instance of a password that needs to be edited
    @param response: some response
    """

    password_to_edit = session.query(DataPassword).where(
        sqlalchemy.and_(
            DataPassword.user_id == user.id, 
            DataPassword.address == password.address
        )
    ).first()

    if not password_to_edit:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.PASSWORD_NOT_EXIST

    data = {
        "service": password.service,
        "login": password.login,
        "password": password.password
    }

    resp = requests.post(f"{IPFS_URL}/api/v0/add", files={
        sha512((password.service + password.login + password.password + password.public_key).encode("utf-8")).hexdigest(): json.dumps(data)
    })

    if resp.status_code != 200:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorTypes.FAILED_ADD_PASSWORD_TO_IPFS

    new_address = resp.json()["Hash"]

    password_to_edit.address = new_address
    session.commit()

    session.close()

    return new_address

