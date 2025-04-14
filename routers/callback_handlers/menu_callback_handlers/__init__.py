from aiogram import Router

from .menu_callback_handlers import router as menu_callback_router


router = Router(name=__name__)
router.include_router(menu_callback_router)