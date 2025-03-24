__all__ = ("router",)
from .handlers import router as handlers_router

from  aiogram import Router

router = Router(name="product")
router.include_router(handlers_router)