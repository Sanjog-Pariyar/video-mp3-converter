from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, queue

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(queue.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}