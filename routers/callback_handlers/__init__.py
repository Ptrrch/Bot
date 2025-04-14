from aiogram import Router
from .admins_callback_handlers import router as admin_callback_router
from .cities_callback_handlers import router as cities_callback_router
from .kitchens_callback_handlers import router as kitchen_callback_router
from .product_callback_handlers import router as product_callback_router
from .client_callback_handlers import router as client_callback_router
from .couriers_callback_handlers import router as courier_callback_router
from .menu_callback_handlers import router as menu_callback_router
from .user_callback_handlers import router as user_callback_router

router = Router(name="callback_admin")

router.include_routers(
    admin_callback_router,
    cities_callback_router,
    kitchen_callback_router,
    product_callback_router,
    client_callback_router,
    courier_callback_router,
    menu_callback_router,
    user_callback_router)
