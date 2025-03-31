# from aiogram import Router, F
# from aiogram.types import CallbackQuery
#
# from Keyboards.Menu_kb import CartActions, CartCbData
#
# router = Router(name=__name__)
#
#
# @router.callback_query(
#     CartCbData.filter(F.action == CartActions.back),
# )
# async def delete_list_kitchen_menu(call: CallbackQuery):
#     await call.message.delete()
#
# @router.callback_query(
#     CartCbData.filter(F.action == CartActions.show),
# )
# async def get_product_menu_keyboards(call: CallbackQuery, callback_data:MenuFirstCbData):
#     products = await get_products({'owned_id':callback_data.kitchen_id})
#     product = []
#     for item in products:
#         product.append(item)
#
#     keyboard = create_product_menu(product[0].id, True, False, position=0, kitchen_id=callback_data.kitchen_id)
#     await call.message.answer_photo(photo=product[0].img, caption=product[0].description, reply_markup=keyboard)
#
#
# @router.callback_query(
#     MenuSecondCbData.filter(F.action == MenuSecondActions.back),
# )
# async def delete_product_menu_keyboards(call: CallbackQuery):
#     await call.message.delete()
#
# @router.callback_query(
#     MenuSecondCbData.filter(F.action == MenuSecondActions.next),
# )
#
# async def move_next_product_menu_keyboards(call: CallbackQuery, callback_data:MenuSecondCbData):
#     products = await get_products({'owned_id':callback_data.kitchen_id})
#     product = []
#     is_last = False
#     count_item = 0
#
#     for item in products:
#         product.append(item)
#         count_item += 1
#
#     current_product = product[callback_data.position]
#
#     next_item = callback_data.position + 1
#
#     if next_item == count_item - 1:
#         is_last = True
#
#     if next_item <= count_item:
#         current_product = product[next_item]
#     keyboard = create_product_menu(current_product.id, False, is_last, position=next_item, kitchen_id=callback_data.kitchen_id)
#     media = InputMediaPhoto(media=current_product.img,caption=current_product.description)
#     await call.message.edit_media(media=media, reply_markup=keyboard)
#
#
# @router.callback_query(
#     MenuSecondCbData.filter(F.action == MenuSecondActions.last),
# )
# async def move_last_product_menu_keyboards(call: CallbackQuery, callback_data: MenuSecondCbData):
#     products = await get_products({'owned_id': callback_data.kitchen_id})
#     product = []
#     is_first = False
#     count_item = 0
#
#     for item in products:
#         product.append(item)
#         count_item += 1
#
#     current_product = product[callback_data.position]
#
#     last_item = callback_data.position - 1
#
#     if last_item == 0:
#         is_first = True
#     if last_item >= 0:
#         current_product = product[last_item]
#     keyboard = create_product_menu(current_product.id, is_first, False, position=last_item,
#                                    kitchen_id=callback_data.kitchen_id)
#     media = InputMediaPhoto(media=current_product.img,caption=current_product.description)
#     await call.message.edit_media(media=media, reply_markup=keyboard)