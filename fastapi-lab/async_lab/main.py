from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from data import get_async_db, Base,engine
from sqlalchemy import text, Select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User


app = FastAPI()

Base.metadata.create_all(bind=engine)



class user(BaseModel):
    name: str
    age: int


@app.get('/test')
async def test_db(db : AsyncSession = Depends(get_async_db)):
    result = await db.execute(text('SELECT 1'))

    return {
        "result": result.scalar_one()
    }

@app.get('/users')
async def get_users(db : AsyncSession= Depends(get_async_db)):
    
    stmt = Select(User)
    result = await db.execute(stmt)

    return result.scalars().all()

@app.post('/users')
async def create_user(u: user, db: AsyncSession= Depends(get_async_db)):
    new_usr = User(
        name= u.name,
        age = u.age
    )
    db.add(new_usr)
    await db.commit()
    await db.refresh(new_usr)

    return new_usr

@app.put('/users/{id}')
async def update_user(id: int, u: user, db: AsyncSession= Depends(get_async_db)):
    stmt = Select(User).where(User.id == id)
    usr_obj = await db.execute(statement=stmt)
    usr = usr_obj.scalars().first()

    if usr:
        usr.name = u.name
        usr.age = u.age

        await db.commit()
        await db.refresh(usr)

        return usr

    raise HTTPException(404, 'user not found')

    


