from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql+psycopg2://my_fastapi_user:password1234@localhost:5432/fastapi_db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

session_local = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()