__all__ = ("router",)


from  aiogram import Router
from .base_commands import router as base_commands_router
from .city_commands import router as city_keyboard_router

router = Router()
router.include_router(city_keyboard_router)
router.include_router(base_commands_router)


