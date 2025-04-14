from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import AdminCourierCbData, AdminCourierActions, get_couriers_for_admin_keyboards
from Keyboards.Courier_kb import create_courier_interface, CourierItemCbData, CourierActions, CourierOrderCb, \
    CourierOrderActions, courier_change_profile, courier_order_delivered_interface
from database.crud.cities_crud import get_one_city
from database.crud.couriers_crud import get_courier, delete_courier, get_couriers
from database.crud.orders_crud import change_state_order
from database.models import StateOrder
from filters.isCourier import CourierFilter

router = Router(name=__name__)
router.message.filter(CourierFilter())

@router.message(F.text == '📚 Курьер', CourierFilter())
async def show_kitchen_interface(message: types.Message):
    title = "-"
    courier = await get_courier(message.from_user.id)
    city = await get_one_city(courier.city_id)
    if city:
        title = city.title
    text = f"""
    Ваш профиль:\nИмя: {courier.name}\nФамилия: {courier.lastname}\nГород: {title}\nНомер телефона: {courier.number}
    """
    await message.answer(text, reply_markup=courier_change_profile(courier.user_id))

@router.callback_query(
    AdminCourierCbData.filter(F.action == AdminCourierActions.details)
)
async def show_info_courier(call: CallbackQuery, callback_data: AdminCourierCbData):
    courier = await get_courier(callback_data.user_id)
    text = markdown.text(
        markdown.hbold(f"{courier.name}\n"),
            markdown.hbold(f"{courier.lastname}\n"),
            markdown.hbold(courier.number)

    )
    await call.message.edit_text(text, reply_markup=create_courier_interface(callback_data.user_id, callback_data.name))

@router.callback_query(
    CourierItemCbData.filter(F.action == CourierActions.delete)
)
async def delete_courier_handlers(call: CallbackQuery, callback_data: AdminCourierCbData):
    await delete_courier(callback_data.id)
    couriers = await get_couriers()
    keyboard = get_couriers_for_admin_keyboards(couriers)
    await call.message.edit_text(
        text="Список курьеров:",
        reply_markup=keyboard,
    )
@router.callback_query(
    CourierOrderCb.filter(F.action == CourierOrderActions.inTheWay)
)
async def delivered_handlers(call: CallbackQuery, callback_data: CourierOrderCb):
    await call.answer()
    await change_state_order(callback_data.order_id, StateOrder.inTheWay)
    await call.message.bot.send_message(callback_data.client_id, "Ваш заказ уже в пути")
    await call.message.edit_reply_markup(reply_markup=courier_order_delivered_interface(callback_data.order_id, callback_data.client_id))

@router.callback_query(
    CourierOrderCb.filter(F.action == CourierOrderActions.delivered)
)
async def delivered_handlers(call: CallbackQuery, callback_data: CourierOrderCb):
    await call.answer()
    await change_state_order(callback_data.order_id, StateOrder.delivered)
    await call.message.bot.send_message(callback_data.client_id, "Надеемся, вам все понравилось😊")
    await call.message.delete()

