from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import (
    AdminActions,
    AdminCbData,
    get_client_for_admin_keyboards,
    get_couriers_for_admin_keyboards, get_cities_for_admin_keyboards, get_kitchens_for_admin_keyboards,
    create_admin_keyboard
)
from database.crud.cities_crud import get_city
from database.crud.clients_crud import get_clients
from database.crud.couriers_crud import get_couriers
from database.crud.kitchens_crud import get_kitchens

router = Router(name=__name__)


@router.callback_query(
    AdminCbData.filter(F.action == AdminActions.back),
)
async def get_admin_keyboards(call: CallbackQuery):
    await call.answer()
    keyboard = create_admin_keyboard()
    await call.message.edit_text(
        text="Привет админ",
        reply_markup=keyboard,
    )

@router.callback_query(
    AdminCbData.filter(F.action == AdminActions.clients),
)
async def get_inline_list_client(call: CallbackQuery):
    await call.answer()
    clients = await get_clients()
    keyboard = get_client_for_admin_keyboards(clients)
    await call.message.edit_text(
        text="Список клиентов:",
        reply_markup=keyboard,
    )

@router.callback_query(
    AdminCbData.filter(F.action == AdminActions.cities),
)
async def get_inline_list_cities(call: CallbackQuery):
    await call.answer()
    cities = await get_city()
    keyboard = get_cities_for_admin_keyboards(cities)
    await call.message.edit_text(
        text="Список Городов:",
        reply_markup=keyboard,
    )


@router.callback_query(
    AdminCbData.filter(F.action == AdminActions.couriers),
)
async def get_inline_list_courier(call: CallbackQuery):
    await call.answer()
    couriers = await get_couriers()
    keyboard = get_couriers_for_admin_keyboards(couriers)
    await call.message.edit_text(
        text="Список курьеров:",
        reply_markup=keyboard,
    )


@router.callback_query(
    AdminCbData.filter(F.action == AdminActions.kitchens),
)
async def get_inline_list_kitchens(call: CallbackQuery):
    await call.answer()
    kitchens = await get_kitchens()
    keyboard = get_kitchens_for_admin_keyboards(kitchens)
    await call.message.edit_text(
        text="Список Заведений:",
        reply_markup=keyboard,
    )


@router.callback_query(
    AdminCbData.filter(F.action == AdminActions.orders),
)
async def get_inline_list_orders(call: CallbackQuery):
    await call.answer()
    # clients = await get_clients()
    # keyboard = get_client_for_admin_keyboards(clients)
    # await call.message.edit_text(
    #     text="Список клиентов:",
    #     reply_markup=keyboard,
    # )




# @router.callback_query(
#     ShopCbData.filter(F.action == ShopActions.root),
# )
# async def handle_my_address_button(call: CallbackQuery):
#     await call.answer()
#     await call.message.edit_text(
#         text="Your shop actions:",
#         reply_markup=build_shop_kb(),
#     )
#
#
# @router.callback_query(
#     ShopCbData.filter(F.action == ShopActions.address),
# )
# async def handle_my_address_button(call: CallbackQuery):
#     await call.answer(
#         "Your address section is still in progress...",
#         cache_time=30,
#     )
#
#
# @router.callback_query(
#     ProductCbData.filter(F.action == ProductActions.details),
# )
# async def handle_product_details_button(
#     call: CallbackQuery,
#     callback_data: ProductCbData,
# ):
#     await call.answer()
#     message_text = markdown.text(
#         markdown.hbold(f"Product №{callback_data.id}"),
#         markdown.text(
#             markdown.hbold("Title:"),
#             callback_data.title,
#         ),
#         markdown.text(
#             markdown.hbold("Price:"),
#             callback_data.price,
#         ),
#         sep="\n",
#     )
#     await call.message.edit_text(
#         text=message_text,
#         reply_markup=product_details_kb(callback_data),
#     )
#
#
# @router.callback_query(
#     ProductCbData.filter(F.action == ProductActions.update),
# )
# async def handle_product_update_button(
#     call: CallbackQuery,
#     callback_data: ProductCbData,
# ):
#     await call.answer()
#     await call.message.edit_reply_markup(
#         reply_markup=build_update_product_kb(callback_data),
#     )
#
#
# @router.callback_query(
#     ProductCbData.filter(F.action == ProductActions.delete),
# )
# async def handle_product_delete_button(
#     call: CallbackQuery,
# ):
#     await call.answer(
#         text="Delete is still in progress...",
#     )
#
