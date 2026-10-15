from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "Hello world, this is fastapi"}

@app.get("/about")
def about():
    return "This is the about page"

@app.get("/user/{id}")
def get_user(id: int):
    return {"user ID": id}

@app.get("/query")
def get_query(name: str = "james", id: int=10, age:int= 20):
    return {
        "name": name,
        "age": age,
        "ID": id
    }


class calculation(BaseModel):
    num1 : float
    num2 : float
    operator : str

class response(BaseModel):
    result : float
    
@app.post("/calculate", response_model=response)
def calculate(data : calculation):
    operators = ['+', '-', '*', '/', '%']
    if data.operator == '/' and data.num2 == 0:
        raise HTTPException(400, "Division by zero is impossible")
    if data.operator not in operators:
        raise HTTPException(400, "invalid operator")
    
    res = calc(data.num1, data.num2, data.operator)
    return {"result": res}



class User(BaseModel):
    name: str
    age: int

# PUT request 
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    return {
        "id": user_id,
        "name": user.name,
        "age": user.age
    }






def calc(a, b, operator)->int:
    if operator == "+":
        return a+b
    elif operator == "-":
        return a-b
    elif operator == "/":
        return a/b
    elif operator == "*":
        return a*b
    elif operator == "%":
        return a%b