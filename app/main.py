
from fastapi import FastAPI
from app.api import devices, users
from app.middleware.time_middleware import TimerMiddleware

app = FastAPI()

app.add_middleware(TimerMiddleware)
app.include_router(devices.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

