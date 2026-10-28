from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

db_URL = 'postgresql+psycopg2://my_fastapi_user:password1234@localhost:5432/fastapi_db'

async_db_URL = 'postgresql+asyncpg://my_fastapi_user:password1234@localhost:5432/fastapi_db'

engine = create_engine(db_URL)

async_engine = create_async_engine(async_db_URL)

Base = declarative_base()

sessionLocal = sessionmaker(
    bind=engine, 
    autoflush= False,
    autocomit = False
)

asyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_= AsyncSession,
    expire_on_commit= False
)

def get_db():
    db = sessionLocal()

    try:
        yield db

    finally:
        db.close()


async def get_async_db():

    async with asyncSessionLocal() as db:
       
        yield db



