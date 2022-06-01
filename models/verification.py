from pydantic import BaseModel


class VerificationModel(BaseModel):
    """Verification classs for users."""

    public_key: str
    verification_string: str
    signature: str

