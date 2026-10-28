from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

db_url = "postgresql+psycopg2://my_fastapi_user:password1234@localhost:5432/fastapi_db"

async_db_url = "postgresql+asyncpg://my_fastapi_user:password1234@localhost:5432/fastapi_db"

Base = declarative_base()

engine = create_engine(db_url)

async_engine = create_async_engine(async_db_url, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

async_sessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_= AsyncSession
)


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


async def get_async_db():

    async with async_sessionLocal as session:
        yield session

