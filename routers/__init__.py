__all__ = ("router",)

from aiogram import Router

from .commands import router as commands_router
from .client import router as client_router
from .admin import router as admin_router
from .city import router as city_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    client_router,
    admin_router,
    city_router
)

