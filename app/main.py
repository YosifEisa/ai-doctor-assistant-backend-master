import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import (
    auth,
    users,
    family_members,
    allergies,
    chronic_diseases,
    lab_scan_tests,
    health_profile,
    medications,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for AI Doctor Assistant application",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(family_members.router)
app.include_router(allergies.router)
app.include_router(chronic_diseases.router)
app.include_router(lab_scan_tests.router)
app.include_router(health_profile.router)
app.include_router(medications.router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API health check."""
    return {
        "message": "Welcome to AI Doctor Assistant API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)