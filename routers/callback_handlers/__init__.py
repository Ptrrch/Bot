from aiogram import Router
from .admins_callback_handlers import router as admin_callback_router
from .cities_callback_handlers import router as cities_callback_router
from .kitchens_callback_handlers import router as kitchen_callback_router
from .product_callback_handlers import router as product_callback_router

router = Router(name="callback_admin")

router.include_routers(
    admin_callback_router,
    cities_callback_router,
    kitchen_callback_router,
    product_callback_router)
