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


@router.post("/initUser/", status_code=status.HTTP_200_OK)
def init_user(user: InitUserModel, response: Response):
    session = db_session.create_session()
    # Load sent public key
    pub_key = serialization.load_pem_public_key(
        unhexlify(user.public_key)
    )

    try:
        if len(user.verification_string) != 128:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "Verification string length should be 128"
        # Verify signature
        pub_key.verify(
            unhexlify(user.signature),
            unhexlify(user.verification_string),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        )
        
        # Find user in database
        if db_user := session.query(User).where(User.public_key == user.public_key).first():
            passwords: List[Password] = session.query(Password).where(Password.user_id == db_user.id).all()
            # Get passwords from ipfs and return
        else:
            # Create new user
            new_user = User()
            new_user.public_key = user.public_key
            session.add(new_user)
            session.commit()
            return "{}"
    except InvalidSignature:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Invalid signature"
