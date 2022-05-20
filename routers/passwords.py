from fastapi import APIRouter, Response, status
from models.password import Password


router = APIRouter(prefix="/api")


@router.post("/add_password", status_code=status.HTTP_200_OK)
def add_password(password: Password):
    print(password)
