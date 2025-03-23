# src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import app_routes

app = FastAPI(
    title="App Analytics API",
    description="REST API to serve processed App Store data",
    version="1.0.0"
)

# Optional: allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Alterar para o domínio do frontend em prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(app_routes.router)

# Healthcheck route
@app.get("/")
async def root():
    return {"message": "📡 App Analytics API is up and running"}
