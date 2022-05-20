from models.verification import VerificationModel


class PasswordDelete(VerificationModel):
	"""
	address - address of password in IPFS
	"""

	address: str