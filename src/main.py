from fastapi import FastAPI

http_app = FastAPI()

@http_app.get("/")
def welcome():
    return {"message": "Hello World"}

@http_app.get("/askthing")
def httpaction():
    return {"message": "You did the thing"}