from pydantic import BaseModel


class InitUserModel(BaseModel):
    public_key: str
    verification_string: str
    signature: str
