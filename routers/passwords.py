from fastapi import APIRouter, Response, status
from models.password import Password
from models.errors import ErrorTypes
from data import db_session
from data.users import User
import data.passwords as dpasswords
from routers.auth import verify_signature
import requests
import json
from hashlib import sha512


router = APIRouter(prefix="/api")


@router.post("/add_password", status_code=status.HTTP_200_OK)
def add_password(password: Password, response: Response):
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
    pwd = dpasswords.Password()
    pwd.user_id = user.id
    pwd.address = addr
    session.add(pwd)
    session.commit()

    return addr
    
