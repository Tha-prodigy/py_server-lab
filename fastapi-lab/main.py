from data import get_db, Base, engine
from models import User, Post
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app= FastAPI()

class user_create(BaseModel):
    name : str
    age : int

class user_patching(BaseModel):
    name : str|None= None
    age : int| None = None

# create model for post
class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


@app.get("/users")
def get_users(db : Session = Depends(get_db)):
#    users = db.query(User).all()

#    return users

    stmt =select(User)
    res = db.execute(stmt).scalars().all()
    return [{"name" : user.name, "age": user.age} for user in res]

@app.get('/user/{id}')
def get_user(id: int, db : Session= Depends(get_db)):
    stmt = select(User).where(User.id == id)
    user = db.execute(stmt).scalars().first()
    return user



@app.post('/users') 
def create_user(user: user_create, db: Session= Depends(get_db)):
    new_user = User(
        name = user.name,
        age = user.age
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.put("/users/{id}")
def change_user(id: int, user: user_create, db: Session= Depends(get_db)):
    current_user = db.query(User).filter(User.id == id).first()
    if current_user is not None:
       current_user.name = user.name
       current_user.age = user.age
       db.commit()
       db.refresh(current_user)
       return current_user

    else:
        raise HTTPException(404, "User not found")

    
@app.patch('/users/{id}')
def modify_user_detail(id : int, user: user_patching, db: Session= Depends(get_db)):
    current_user = db.query(User).filter(User.id == id).first()
    if current_user is None:
        raise HTTPException(400, "user not found")

    if user.name is not None:
        current_user.name = user.name
    if user.age is not None:
        current_user.age = user.age
   
    db.commit()
    db.refresh(current_user)

    return current_user


@app.delete('/users/{id}')
def delete_user(id: int, db : Session= Depends(get_db)):
    current_user = db.query(User).filter(User.id == id).first()
    if current_user is None:
        raise HTTPException(404, "user not found")

    db.delete(current_user)
    db.commit()

    return {"status": "Deletion successful", "user":current_user}


# ======================= Post ENDPOINT ===============================


@app.post('/posts')
def create_post(post: PostCreate, db: Session= Depends(get_db)):
    user_post = Post(
        title= post.title,
        content= post.content,
        user_id= post.user_id  
        )

    db.add(user_post)
    db.commit()
    db.refresh(user_post)

    return user_post


@app.get('/users/{id}/post')
def get_user_post(id: int, db : Session= Depends(get_db)):
    current_user= db.query(User).filter(User.id==id).first()

    if current_user is not None:
        return [{"title": post.title, "content": post.content, "user_id": post.user_id} for post in current_user.posts]

    raise HTTPException('404', "user not found")


@app.get('/posts/{id}')
def get_post(id: int, db: Session= Depends(get_db)):
    # user = db.query(User).filter(User.id == id).first()
    # if user == None:
    #     raise HTTPException(404, "user not found")

    # return [{"post-title": post.title, "autor": post.user.name} for post in user.posts]


    # post = db.query(Post).filter(Post.id == id).first()
    stmt = select(Post).where(Post.id==id)
    post = db.execute(stmt).scalars().first()
    if not post:
        raise HTTPException(404, "user not found")

    return {
        "post-title": post.title,
        "author": post.user.name
    }

@app.get('/posts')
def get_post_id(db: Session= Depends(get_db)):
    # result = db.query(User.name, Post.title).join(Post).all()
    
    # return [{"name": name, "title": title} for name, title in result]


   
    stmt = select(User.name, Post.title).join(Post)
    res =db.execute(stmt).all()
    print(res)






    
   
           



