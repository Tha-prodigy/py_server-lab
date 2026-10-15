from data import Base
from sqlalchemy import Integer, String, Column


class User(Base):
    __tablename__ = 'async_users'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    age = Column(Integer)

