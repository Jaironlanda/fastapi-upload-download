from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import v1
from .v1 import main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(v1.main.router)
