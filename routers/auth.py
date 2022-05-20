import binascii
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from fastapi import APIRouter, Response, status
from data.users import User
from data.passwords import Password
from data import db_session
from models.init_user_model import InitUserModel
from binascii import unhexlify
from typing import List


router = APIRouter(prefix="/api")


def verify_signature(model):
    # Load public key
    pub_key = serialization.load_pem_public_key(
        unhexlify(model.public_key)
    )
    # Check verification string length
    if len(model.verification_string) != 256:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Verification string length should be 256"
    try:
        # Verify signature
        pub_key.verify(
            unhexlify(model.signature),
            unhexlify(model.verification_string),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        )
        return True
    except InvalidSignature:
        return False


@router.post("/init_user/", status_code=status.HTTP_200_OK)
def init_user(user: InitUserModel, response: Response):
    session = db_session.create_session()
    verification_check = verify_signature(user)

    if verification_check is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Invalid signature"
        
    # Find user in database
    if (db_user := session.query(User).where(User.public_key == user.public_key).first()) is None:
        # Create new user
        new_user = User()
        new_user.public_key = user.public_key
        session.add(new_user)
        session.commit()
