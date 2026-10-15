from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker



db_URL = "postgresql+psycopg2://my_fastapi_user:password1234@localhost:5432/fastapi_db"
async_db_URL = "postgresql+asyncpg://my_fastapi_user:password1234@localhost:5432/fastapi_db"

engine = create_engine(db_URL)

# ========== CREATE SYNC SESSION ===============
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

#  =========== CREATE ASYNC SESSION ==============

async_engine = create_async_engine(async_db_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind= async_engine,
    class_= AsyncSession,
    expire_on_commit=False

)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
