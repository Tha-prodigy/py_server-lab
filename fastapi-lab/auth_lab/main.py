from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, FastAPI
from pydantic import BaseModel
from data import Base, engine, get_async_db
from model import User
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






fake_user = {
    "username": "daniel",
    "password": "mypassword123",
    "id": 1
}

class CreateUser(BaseModel):
    name : str
    password: str
    age: int


@app.post('/register')
async def register_route(usr: CreateUser, db : AsyncSession= Depends(get_async_db)):
    new_user = User(
        name = usr.name,
        password = hash_password(usr.password),
        age = usr.age
        
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

    
    



@app.post('/login', response_model=Token)
async def login_user(form_data : OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user['username'] or form_data.password != fake_user['password']:
        raise HTTPException(401, 'Incorrect username or password', {'WWW-Authenticate': 'Bearer' })

    access_token = create_access_token({'sub': str(fake_user['id'])})

    return {
        'access_token': access_token,
        "token_type": 'bearer'
    }


@app.get('/proctected')
async def protected_route(credentials: HTTPAuthorizationCredentials=Depends(security)):
    token = credentials.credentials
    print(token)

    try:
        payload = jwt.decode(token, secret_key, algorithm)

        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code= 401, detail={'message': 'You are not authorized'}, headers={'WWW-Authenticate': 'Bearer'})

        return {
            'message': 'You have authorization',
            'user-id': user_id
        }

    except jwt.InvalidTokenError:
        raise HTTPException(
            401,
            {'message': 'invalid or expired token '},
            headers={'WWW-Authenticate': 'Bearer'}
        )

    




