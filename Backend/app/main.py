from fastapi import FastAPI, Request
from app.middleware.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routes.travel import router as travel_router

app = FastAPI(title="Travel Intelligence Engine")

# Configure rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.include_router(travel_router)


@app.get("/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    return {"status": "ok"}
