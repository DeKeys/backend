from fastapi import APIRouter, Response, status
from hashlib import sha512
import sqlalchemy
import requests
import json

from models.user import UserModel
from models.password import Password
from models.password_delete import PasswordDelete
from models.error_types import ErrorTypes

from data import db_session
from data.users import User
import data.passwords as data_passwords

from routers.auth import verify_signature


router = APIRouter(prefix="/api")


@router.post("/create_password", status_code=status.HTTP_200_OK)
def create_password(password: Password, response: Response):
    """
    TODO: - Add documentation
    """

    # Verify signature
    session = db_session.create_session()
    if verification_check := verify_signature(password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return verification_check

    # Check if user exists
    user = session.query(User).where(User.public_key == password.public_key).first()
    if user is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.ACCOUNT_NOT_EXISTS

    # Add password to IPFS
    data = {
        "service": password.service,
        "login": password.login,
        "password": password.password
    }

    resp = requests.post("http://127.0.0.1:5001/api/v0/add", files={
        sha512((password.service + password.login + password.password + password.public_key).encode("utf-8")).hexdigest(): json.dumps(data)
    })
    if resp.status_code != 200:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorTypes.FAILED_ADD_PASSWORD_TO_IPFS
    addr = resp.json()["Hash"]

    # Add password to database
    pwd = data_passwords.Password()
    pwd.user_id = user.id
    pwd.address = addr
    session.add(pwd)
    session.commit()

    return addr


# Password Deletion  
@router.post("/delete_password", status_code=status.HTTP_200_OK)
def delete_password(password: PasswordDelete, response: Response):
    """
    TODO: - Add documentation
    """

    # Verify signature
    session = db_session.create_session()
    if verification_check := verify_signature(password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return verification_check

    # Check if user exists
    user = session.query(User).where(User.public_key == password.public_key).first()
    if user is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.ACCOUNT_NOT_EXISTS

    # Get password from database
    users_password = session.query(data_passwords.Password).where(
        sqlalchemy.and_(
            data_passwords.Password.user_id == user.id, 
            data_passwords.Password.address == password.address
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
def get_password(user: User, response: Response):
    """
    TODO: - Add documentation
    """

    # Verify signature
    session = db_session.create_session()
    if verification_check := verify_signature(password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return verification_check

    # Check if user exists
    user = session.query(User).where(User.public_key == password.public_key).first()
    if user is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.ACCOUNT_NOT_EXISTS
    passwords = session.query(Password).where(Password.user_id == user.id).all() 
    return json.dumps({
        "passwords": passwords    
    })
