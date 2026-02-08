"""Routes package."""
from .cv import router as cv_router
from .job import router as job_router
from .tailor import router as tailor_router
from .write import router as write_router
from .process import router as process_router

__all__ = ["cv_router", "job_router", "tailor_router", "write_router", "process_router"]
