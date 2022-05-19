from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase
from binascii import hexlify


class User(SqlAlchemyBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    public_key = Column(String, unique=True)
