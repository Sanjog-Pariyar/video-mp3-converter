from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import users, login

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://gateway:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(login.router)

@app.get("/")
def get_root():
    return {"message": "Auth Service API"}