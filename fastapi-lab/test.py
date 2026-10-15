from fastapi import FastAPI, Request, Depends, Header
from datetime import datetime



# @app.get('/')
# def tester(content_type: str | None = Header(default=None)):
#     return {
#         "content-type": content_type
#     }


# @app.get('/')
# def tester(request : Request):
#     return{
#         "user-agent" : request.headers.get('user-agent'),
#         "content-type": request.headers.get('content-type')
#     }

apple = FastAPI()


# def client(authorization : str|None= Header()):
#     return authorization

# @apple.get("/")
# def get_time(cl_name : str|None= Depends(client)):
#     return {"client_name": cl_name}

def token():
    return "abcd321"

def get_current_user(token= Depends(token)):
    return{
        "name": "James",
        "token": token
    }

@apple.get("/profile")
def get_profile(profile= Depends(get_current_user)):
    return profile


    