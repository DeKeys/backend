from pydantic import BaseModel


class VerificationModel(BaseModel):
    public_key: str
    verification_string: str
    signature: str

