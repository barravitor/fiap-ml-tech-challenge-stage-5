from fastapi import APIRouter
from .app_routes import app_router
from .public_routes import public_router
from .private_routes import private_router

router = APIRouter()

router.include_router(public_router, prefix="/api/public", tags=["API Public Routes"])
router.include_router(private_router, prefix="/api/private", tags=["API Private Routes"])
router.include_router(app_router, prefix="/app", tags=["App Routes"])
