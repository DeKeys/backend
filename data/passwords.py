from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
import datetime
from .db_session import SqlAlchemyBase


class Password(SqlAlchemyBase):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String)
    created_at = Column(DateTime, default=datetime.datetime())

