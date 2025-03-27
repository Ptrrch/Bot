from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import AdminKitchensCbData, AdminKitchensActions, get_kitchens_for_admin_keyboards
from Keyboards.Kitchen_kb import create_kitchen_keyboard, KitchenItemCbData, KitchenActions
from database.crud.kitchens_crud import delete_kitchen, get_kitchens

router = Router(name=__name__)

@router.callback_query(AdminKitchensCbData.filter(F.action == AdminKitchensActions.details))
async def create_kitchen_details(call:CallbackQuery, callback_data: AdminKitchensCbData):
    text = markdown.text(
        markdown.hbold(f"{callback_data.title}")
    )
    await call.message.edit_text(text=text, reply_markup=create_kitchen_keyboard(callback_data.id, callback_data.title))

@router.callback_query(KitchenItemCbData.filter(F.action == KitchenActions.delete))
async def delete_kitchen_handlers(call: CallbackQuery, callback_data: KitchenItemCbData):
    await delete_kitchen(callback_data.id)
    kitchens = await get_kitchens()
    keyboard = get_kitchens_for_admin_keyboards(kitchens)
    await call.message.edit_text(
        text="Список Заведений:",
        reply_markup=keyboard,
    )