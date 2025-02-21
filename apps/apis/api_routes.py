from fastapi import APIRouter

from apps.apis.v1.auth.auth_endpoint import auth_router
from apps.apis.v1.v1_endpoint import v1_router

router = APIRouter()
router.include_router(v1_router, prefix="/v1", tags=["v1_endpoint"])
