from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


users = [{"name": "Daniel", "age": 24, "id": 1}, {"name": "James", "age": 20, "id": 2}]
app = FastAPI()
user_id = len(users)



class User(BaseModel):
    name: str
    age: int

class User_update(BaseModel):
    name: str | None = None
    age: int | None= None


# get user handler
@app.get('/users')
def get_users():
    return users

# create user
@app.post('/users')
def create_user(user: User):
    global user_id
    user_id +=1

    u = {'name': user.name, 'age': user.age, "id": user_id}
    users.append(u)

    return u

@app.put('/users/{id}')
def change_user(id: int, u: User):
    for user in users:
        if user["id"] == id:
            user['name'] =u.name
            user['age'] = u.age
            # print(user["name"], u.name)

            return {
                "status": "update successful",
                "new_name": u.name,
                "new_age": u.age
            }
        else:
            continue

    raise HTTPException(404, "user not found")

@app.patch('/users/{id}')
def modify_user_detail(id: int, u: User_update):
    for user in users:
        if user['id'] == id:

            if u.name is not None:
                user['name'] = u.name

            if u.age is not None:
                user['age']= u.age

            return user

    raise HTTPException(404, 'user not found...')

@app.delete('/users/{id}')
def delete_user(id: int):
    for user in users:
        if user['id'] == id:
            users.remove(user)
            return user
        
    raise HTTPException(404, 'user not found...')
    






