from sqlalchemy import Column, Integer, String, Text

from ..db_setup import Base
from .mixins import Timestamp

# class Base(AsyncAttrs, DeclarativeBase):
#     pass


class User(Timestamp, Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
