from aiogram import Router
from .admins_callback_handlers import router as admin_callback_router

router = Router(name="callback_admin")

router.include_router(admin_callback_router)
