from models.verification import VerificationModel


class PasswordEdit(VerificationModel):
	"""
	address - address of password in IPFS
	"""

	address: str
	service: str
	login: str
	password: str