import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.routes import app_routes, analysis_routes
from src.core.config import settings
from src.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler  # correto para versões atuais

# Global logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan hook for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 API is starting up...")
    logger.info(f"✅ ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS} ({type(settings.ALLOWED_ORIGINS)})")
    yield
    logger.info("🛑 API is shutting down...")

# FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0.0",
    lifespan=lifespan,
    redirect_slashes=False
)

# ✅ CORS middleware deve vir primeiro
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Routers
app.include_router(app_routes.router)
app.include_router(analysis_routes.router)

# Health check
@app.get("/")
async def root():
    return {"message": "📡 App Analytics API is up and running"}
