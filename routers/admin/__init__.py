from aiogram import Router
from .handlers import router as handlers_router

router = Router(name="admin")
router.include_router(handlers_router)