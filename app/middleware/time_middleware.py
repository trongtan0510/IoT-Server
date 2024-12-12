import time
from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f'Time: {process_time}')
        return response