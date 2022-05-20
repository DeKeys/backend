from models.verification import VerificationModel


class Password(VerificationModel):
    service: str
    login: str
    password: str