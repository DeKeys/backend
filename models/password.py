from models.verification import VerificationModel


class Password(VerificationModel):
    """The class for password creation."""

    service: str
    login: str
    password: str

