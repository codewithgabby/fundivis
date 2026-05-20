import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.limiter import limiter
from app.routers import auth, income, expense, summary, buckets, committed

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Fundivis API",
    description="Multi-user personal finance awareness system",
    version="1.0.0"
)

# CORS - MUST be first middleware (before SlowAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many login attempts. Please try again later."},
    )

app.include_router(auth.router)
app.include_router(income.router)
app.include_router(expense.router)
app.include_router(summary.router)
app.include_router(buckets.router)
app.include_router(committed.router)

# Health check
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Fundivis API is running"
    }