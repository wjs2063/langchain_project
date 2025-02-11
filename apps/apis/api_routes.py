from fastapi import APIRouter
from apps.apis.v1.auth.auth_endpoint import auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["authentication"])
