from fastapi import FastAPI
from app.routers import auth, collections, todos

app = FastAPI()

app.include_router(auth.router)
app.include_router(collections.router)
app.include_router(todos.router)
