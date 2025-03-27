import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import app_routes, analysis_routes
from src.core.config import settings
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Global logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Limiter instance
limiter = Limiter(key_func=get_remote_address)

# Lifespan hook for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 API is starting up...")
    yield
    logger.info("🛑 API is shutting down...")

# FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0.0",
    lifespan=lifespan
)

# Attach rate limiter
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(app_routes.router)
app.include_router(analysis_routes.router)

# Health check route
@app.get("/")
async def root():
    return {"message": "📡 App Analytics API is up and running"}
