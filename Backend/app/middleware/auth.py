from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        api_key = request.headers.get("X-API-KEY")

        if api_key != settings.API_SECRET_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")

        response = await call_next(request)
        return response
