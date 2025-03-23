import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import app_routes
from src.core.config import settings
from contextlib import asynccontextmanager

# Global logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Health check route
@app.get("/")
async def root():
    return {"message": "📡 App Analytics API is up and running"}
