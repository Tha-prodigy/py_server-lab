from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, FastAPI
from pydantic import BaseModel
from data import Base, engine, get_async_db
from model import User, SavedBooks
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text


import jwt
from datetime import datetime, timedelta, timezone




secret_key = 'e2fd13ea1e96f58d2a3f1d5b87db135a48d93245af6fcff86f1030f1c1e542a2'
algorithm = 'HS256'
access_token_expiry_time = 30 


class Token(BaseModel):
    access_token : str
    token_type : str


def create_access_token(data: dict):

    to_encode= data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=access_token_expiry_time)
    to_encode.update({'exp': expires})
     
    return jwt.encode(to_encode, secret_key, algorithm)



app = FastAPI()

Base.metadata.create_all(bind=engine)

security = HTTPBearer()


password_hash = PasswordHash.recommended()

def hash_password(password):

    return password_hash.hash(password)


def verify_password(password, hashed_password)-> bool:
    
    return password_hash.verify(password, hashed_password)






async def get_current_user(credentials: HTTPAuthorizationCredentials= Depends(security), db : AsyncSession= Depends(get_async_db)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, secret_key,algorithms= [algorithm])
        usr_id = payload.get('sub')

        if usr_id == None:
            raise HTTPException(401, 'authentication failed', headers={'WWW-Authenticate': 'Bearer'})

        res = await db.execute(select(User).where(User.id == int(usr_id)))

        usr = res.scalars().first()

        if usr == None:
            raise HTTPException(401, 'User not found')

        return usr

    except jwt.InvalidTokenError:

        raise HTTPException(401, 'invalid or expired token', headers={'WWW-Authenticate': 'Bearer'})
    


class CreateUser(BaseModel):
    name : str
    username : str
    password: str
    age: int

class newUserResp(BaseModel):
    id: int
    name: str
    username: str



@app.post('/register', response_model= newUserResp, status_code=201)
async def register_route(usr: CreateUser, db : AsyncSession= Depends(get_async_db)):

    stmt = select(User).where(User.username== usr.username)
    res = await db.execute(statement=stmt)
    
    # check if username already exists 
    existing_usr = res.scalar_one_or_none()
    if existing_usr:
        raise HTTPException(
            status_code=400,
            detail= 'Username already exists'
        )

    new_user = User(
        name = usr.name,
        username = usr.username,
        password = hash_password(usr.password),
        age = usr.age
        
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

    
    



@app.post('/login', response_model=Token)
async def login_user(form_data : OAuth2PasswordRequestForm = Depends(), db : AsyncSession = Depends(get_async_db)):
    stmt = select(User).where(User.username == form_data.username)
    res = await db.execute(stmt)
    usr = res.scalar_one_or_none()

    if usr == None or not verify_password(form_data.password, usr.password):
        raise HTTPException(401, 'Invalid login credentials', headers={'WWW-Authenticate': 'Bearer'})
        

    access_token = create_access_token({'sub': str(usr.id)})

    return {
        'access_token': access_token,
        "token_type": 'bearer'
    }


@app.get('/proctected')
async def protected_route(current_client = Depends(get_current_user)):
    if current_client:
        return {'message': 'You have been authenticated'}


class SaveBook(BaseModel):
    book_key: str
    author: str
    title: str



@app.post('/save_book')
async def save_book(
    book: SavedBooks,
    current_usr: User = Depends(get_current_user),
    db: AsyncSession= Depends(get_async_db)
):

    select(SaveBook)

    




