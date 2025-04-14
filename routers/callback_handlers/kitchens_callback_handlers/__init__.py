from aiogram import Router

from .kitchens_callback_handlers import router as kitchen_callback_router


router = Router(name=__name__)
router.include_router(kitchen_callback_router)