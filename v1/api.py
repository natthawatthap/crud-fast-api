from fastapi import APIRouter
from v1.endpoints.endpoint import router as endpoint_router

router = APIRouter()

router.include_router(endpoint_router)