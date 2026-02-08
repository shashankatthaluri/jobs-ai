"""Jobs Backend - FastAPI Entry Point.

Phase 1: Master CV Intelligence
Phase 2: Job + Company Intelligence
Phase 3: CV Matching & Tailoring
Phase 4: Writing Layer
Phase 5: MVP UI + End-to-End Wiring
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes.cv import router as cv_router
from routes.job import router as job_router
from routes.tailor import router as tailor_router
from routes.write import router as write_router
from routes.process import router as process_router
from routes.analyze import router as analyze_router
from routes.webhooks import router as webhooks_router


# Initialize FastAPI app
app = FastAPI(
    title="Jobs API",
    description="AI-powered job application assistant",
    version="1.0.0"
)

# Configure CORS
# Allow both localhost:3000 (Next.js) and other potential origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(cv_router)
app.include_router(job_router)
app.include_router(tailor_router)
app.include_router(write_router)
app.include_router(process_router)
app.include_router(analyze_router)  # Multi-step API
app.include_router(webhooks_router)  # Polar.sh webhooks


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Jobs API",
        "version": "1.0.0",
        "phases": [1, 2, 3, 4, 5],
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
