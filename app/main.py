
from fastapi import FastAPI
from app.api import devices, users

app = FastAPI()
app.include_router(devices.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

