from fastapi import FastAPI
from app.middleware.auth import APIKeyMiddleware
from app.middleware.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="Travel Intelligence Engine")

# Add API Key Middleware
app.add_middleware(APIKeyMiddleware)

# Add Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
