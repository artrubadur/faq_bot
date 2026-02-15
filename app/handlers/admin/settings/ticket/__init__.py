from aiogram import Router

from .create import router as create_router
from .root import router as root_router

router = Router()

router.include_router(root_router)
router.include_router(create_router)

__all__ = ["router"]
