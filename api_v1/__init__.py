from fastapi import APIRouter

from .auth.router import router as aut_router
from .service.router import router as service_router

router = APIRouter()
router.include_router(router=aut_router, prefix="/token")
router.include_router(router=service_router, prefix="/currency")
