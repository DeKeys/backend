from models.verification_model import VerificationModel



class Password(VerificationModel):
    service: str
    login: str
    password: str

