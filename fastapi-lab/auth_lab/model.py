from sqlalchemy import Column, String, Integer, ForeignKey
from data import Base


class User(Base):

    __tablename__ = 'users_db'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String, unique=True, nullable=True)
    password = Column(String(100))
    age = Column(Integer)


class SavedBooks(Base):

    __tablename__ = 'saved_books'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users_db.id'))
    book_key = Column(String(100), unique=True)
    title = Column(String(255))
    author = Column(String(255))

