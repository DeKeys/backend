from fastapi import APIRouter, Response, status
from binascii import unhexlify
from typing import List
import binascii

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

from data.users import User
from data.passwords import Password
from data import db_session

from models.error_types import ErrorTypes
from models.user import UserModel


router = APIRouter(prefix="/api")


def verify_signature(model):
    """Signature verification function.

    Firstly, get the public key and then check wether it's correct or not.
    Then verifying this public key by provided signature.

    @param model: model is a verification model
    """

    pub_key = serialization.load_pem_public_key(unhexlify(model.public_key))

    if len(model.verification_string) != 256:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorTypes.INVALID_VERIFICATION_STRING_LENGTH
    
    try:
        pub_key.verify(
            unhexlify(model.signature),
            unhexlify(model.verification_string),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        )
    except InvalidSignature:
        return ErrorTypes.INVALID_SIGNATURE 


@router.post("/init_user/", status_code=status.HTTP_200_OK)
def init_user(user: UserModel, response: Response):
    """User initialization.

    Created DB session and then check if user already exists. 
    If not, creates new one.

    @param user: instance of a user
    @param response: some response
    """

    session = db_session.create_session()

    if verification_check := verify_signature(user):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return verification_check    

    if (db_user := session.query(User).where(User.public_key == user.public_key).first()) is None:
        new_user = User()
        new_user.public_key = user.public_key
        session.add(new_user)
        session.commit()

    session.close()

