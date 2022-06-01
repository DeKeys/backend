from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
import datetime
from .db_session import SqlAlchemyBase


class Password(SqlAlchemyBase):
    """The class of a password."""

    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String)
    created_at = Column(DateTime)

