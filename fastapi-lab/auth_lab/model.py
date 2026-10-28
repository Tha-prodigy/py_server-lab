from sqlalchemy import Column, String, Integer
from data import Base


class User(Base):

    __tablename__ = 'users_db'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    password = Column(String(100))
    age = Column(Integer)
