from dataclasses import dataclass


@dataclass
class ErrorTypes:
    INVALID_SIGNATURE = "Invalid signature"
    ACCOUNT_NOT_EXISTS = "You should create account"
    INVALID_VERIFICATION_STRING_LENGTH = "Verification string length should be 256"
    FAILED_ADD_PASSWORD_TO_IPFS = "Failed to add password to IPFS"
    PASSWORD_NOT_EXIST = "Password doesn't exist"
