from fastapi import APIRouter, Response, status
from hashlib import sha512
import sqlalchemy
import requests
import json
import time
from datetime import datetime

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


@router.post("/create_password", status_code=status.HTTP_200_OK)
def create_password(password: Password, response: Response):
    """
    TODO: - Add documentation
    """

    session = db_session.create_session()

    # Verify signature
    if verification_check := verify_signature(password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return verification_check

    # Check if user exists
    if (user := session.query(User).where(User.public_key == password.public_key).first()) is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.ACCOUNT_NOT_EXISTS

    # Add password to IPFS
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

    # Add password to database
    pwd = DataPassword()
    pwd.user_id = user.id
    pwd.address = addr
    pwd.created_at = datetime.now()
    session.add(pwd)
    session.commit()

    return addr


@router.post("/delete_password", status_code=status.HTTP_200_OK)
def delete_password(password: PasswordDelete, response: Response):
    """
    TODO: - Add documentation
    """

    session = db_session.create_session()

    # Verify signature
    if verification_check := verify_signature(password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return verification_check

    # Check if user exists
    if (user := session.query(User).where(User.public_key == password.public_key).first()) is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.ACCOUNT_NOT_EXISTS

    # Get password from database
    users_password = session.query(DataPassword).where(
        sqlalchemy.and_(
            DataPassword.user_id == user.id, 
            DataPassword.address == password.address
        )
    ).first()

    # Check if password exists
    if not users_password:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.PASSWORD_NOT_EXIST

    # Delete password and save database
    session.delete(users_password)
    session.commit()


@router.get("/get_passwords", status_code=status.HTTP_200_OK)
def get_passwords(user: UserModel, response: Response):
    """
    TODO: - Add documentation
    """

    session = db_session.create_session()

    # Verify signature
    if verification_check := verify_signature(user):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return verification_check

    # Check if user exists
    if (user := session.query(User).where(User.public_key == user.public_key).first()) is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.ACCOUNT_NOT_EXISTS

    # Get passwords addresses from database
    db_passwords = session.query(DataPassword).where(DataPassword.user_id == user.id).order_by(DataPassword.created_at.desc()).all()

    # Retrieve passwords from IPFS
    passwords = []

    for db_pwd in db_passwords:
        response = requests.post(f"{IPFS_URL}/api/v0/cat/" + db_pwd.address)
        if response.status_code == 200:
            data = response.json()
            data["created_at"] = db_pwd.created_at.timestamp()
            data["address"] = db_pwd.address
            passwords.append(data)

    return json.dumps({
        "passwords": passwords 
    })


@router.get("/edit_password", status_code=status.HTTP_200_OK)
def edit_password(password: PasswordEdit, response: Response):
    """
    TODO: - Add documentation
    """

    session = db_session.create_session()

    # Verify signature
    if verification_check := verify_signature(password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return verification_check

    # Check if user exists
    if (user := session.query(User).where(User.public_key == password.public_key).first()) is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.ACCOUNT_NOT_EXISTS

    # Get password from database
    password_to_edit = session.query(DataPassword).where(
        sqlalchemy.and_(
            DataPassword.user_id == user.id, 
            DataPassword.address == password.address
        )
    ).first()

    # Check if password exists
    if not password_to_edit:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.PASSWORD_NOT_EXIST

    # Add password to IPFS
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

    # Edit password to database
    password_to_edit.address = new_address
    session.commit()

    return new_address

