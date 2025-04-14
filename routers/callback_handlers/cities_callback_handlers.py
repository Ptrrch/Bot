from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import AdminCitiesCbData, AdminCitiesActions, get_cities_for_admin_keyboards
from Keyboards.City_kb import create_cities_keyboard, CitiesItemCbData, CitiesActions
from database.crud.cities_crud import delete_city, get_city

router = Router(name=__name__)

@router.callback_query(
    AdminCitiesCbData.filter(F.action == AdminCitiesActions.details)
)
async def cities_item_details(call: CallbackQuery, callback_data: AdminCitiesCbData):
    await call.answer()
    message_text = markdown.text(
            markdown.hbold(f"{callback_data.title}"),
        )
    await call.message.edit_text(text=message_text, reply_markup=create_cities_keyboard(callback_data.id, callback_data.title))


@router.callback_query(
    CitiesItemCbData.filter(F.action == CitiesActions.delete)
)
async def delete_city_item(call: CallbackQuery, callback_data: CitiesItemCbData):
    await call.answer()
    await delete_city({'id':callback_data.id})
    cities = await get_city()
    await call.message.edit_text(text = "Список Городов:", reply_markup=get_cities_for_admin_keyboards(cities))