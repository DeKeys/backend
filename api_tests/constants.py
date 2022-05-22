from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding 
import secrets
import os

SERVER_URL = "http://217.28.228.66:8000/api/{}"
IPFS_URL = "https://ipfs.infura.io/ipfs/{}"
# Load private key
with open(os.path.join("api_tests", "private.pem"), "rb") as f:
    PRIVATE_KEY = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Load public key
with open(os.path.join("api_tests", "public.pem"), "rb") as f:
    pub_key_string = f.read()
    PUBLIC_KEY = serialization.load_pem_public_key(
        pub_key_string
    )
    PUB_KEY_STRING = pub_key_string.hex()

# Sign data
DATA = secrets.token_bytes(128)
SIGNATURE = PRIVATE_KEY.sign(
    DATA,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA512()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA512()
)

