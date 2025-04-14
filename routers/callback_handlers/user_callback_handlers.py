from aiogram import Router, F
from aiogram.types import CallbackQuery

from Keyboards.Base_kb import UserFormCb, UserFormActions
from Keyboards.Menu_kb import CartActions, CartCbData
from database.crud.user_crud import update_user_form
from database.models import UserForm

router = Router(name=__name__)


@router.callback_query(
    UserFormCb.filter(F.action == UserFormActions.disagree)
)
async def disagree_form_handle(call: CallbackQuery, callback_data = UserFormCb):
    await call.answer()
    id = callback_data.id
    await update_user_form(id, UserForm.disagree)
    await call.message.delete()

@router.callback_query(
    UserFormCb.filter(F.action == UserFormActions.agree)
)
async def agree_form_handle(call: CallbackQuery, callback_data = UserFormCb):
    await call.answer()
    id = callback_data.id
    await update_user_form(id, UserForm.agree)
    await call.message.delete()