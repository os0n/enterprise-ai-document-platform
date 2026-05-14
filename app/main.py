from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.routes.document_routes import (
    router as document_router
)

from app.routes.auth_routes import (
    router as auth_router
)

from app.database.database import engine

from app.database import models


# =========================
# CREATE DATABASE TABLES
# =========================
models.Base.metadata.create_all(
    bind=engine
)


# =========================
# FASTAPI APPLICATION
# =========================
app = FastAPI(

    title="Enterprise AI Document Platform",

    description="""
AI-powered platform for document processing,
invoice extraction, and workflow automation.
""",

    version="1.0.0",

    docs_url="/docs",

    redoc_url=None
)


# =========================
# CORS CONFIGURATION
# =========================
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================
# API ROUTES
# =========================
app.include_router(
    auth_router,

    prefix="/api/v1/auth",

    tags=["Authentication"]
)

app.include_router(
    document_router,

    prefix="/api/v1/documents",

    tags=["Documents"]
)


# =========================
# ROOT ENDPOINT
# =========================
@app.get(
    "/",
    include_in_schema=False
)
async def root():

    return {
        "message": "Enterprise AI Platform API"
    }


# =========================
# HEALTH CHECK
# =========================
@app.get(
    "/health",
    include_in_schema=False
)
async def health_check():

    return {
        "status": "healthy"
    }