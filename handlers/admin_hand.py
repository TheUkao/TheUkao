from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters import Text, Regexp
from aiogram.dispatcher.filters.builtin import IDFilter

from loader import dp
from loader import bot

import keyboards.user_key as key
import keyboards.admin_key as admin_key
import state as st
from utils import database, payments

from config import ADMIN_CHAT



@dp.callback_query_handler(Regexp("withdraw_payment"), IDFilter(chat_id=ADMIN_CHAT))
async def back_main_menu_message_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_id = call.data.split("=")[-1]
    database.reset_balance_withdrawal(user_id)
    await bot.send_message(user_id, "Выплата подтверждена администратором и отправлена на ваш кошелек")

@dp.callback_query_handler(Regexp("withdraw_unpayment"), IDFilter(chat_id=ADMIN_CHAT))
async def back_main_menu_message_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_id = call.data.split("=")[-1]
    database.restore_balance(user_id)
    await bot.send_message(user_id, "Выплата отклонена")