__all__ = ("router",)


from  aiogram import Router
from .base_commands import router as base_commands_router
from .city_commands import router as city_keyboard_router
from .product_commands import router as product_keyboard_router
from .client_commands import router as client_commands_router
from .admin_commands import router as admin_commands_router

router = Router()
router.include_router(client_commands_router)
router.include_router(city_keyboard_router)
router.include_router(base_commands_router)
router.include_router(product_keyboard_router)
router.include_router(admin_commands_router)

