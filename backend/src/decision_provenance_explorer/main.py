"""
Decision Provenance Explorer - FastAPI Backend
Provides REST API for the decision-provenance library with POKT RPC integration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .api import records, anchors, config, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="Decision Provenance Explorer API",
    description="REST API for tamper-evident ML decision provenance with on-chain verification",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(records.router, prefix="/records", tags=["records"])
app.include_router(anchors.router, prefix="/anchors", tags=["anchors"])
app.include_router(config.router, prefix="/config", tags=["config"])


@app.get("/")
async def root():
    return {
        "name": "Decision Provenance Explorer API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }
