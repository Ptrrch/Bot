__all__ = ("router",)
from  aiogram import Router

from .handlers import router as kitchen_routers

router = Router(name=__name__)

router.include_router(kitchen_routers)

