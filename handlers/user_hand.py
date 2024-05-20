from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters import Text, Regexp

from loader import dp
from loader import bot

import keyboards.user_key as key
import keyboards.admin_key as admin_key
import state as st
from utils import database, payments

from config import ADMIN_CHAT



@dp.message_handler(commands=["start"], state="*")
async def start_message_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.delete()
    if not database.check_reg_user(message.from_user.id):
        database.reg_user(message.from_user.id)
    with open("images/main_page.jpg", "rb") as img:
        await message.answer_photo(photo=img, reply_markup=key.start_key())

@dp.callback_query_handler(Text("back_main_menu"), state="*")
async def back_main_menu_message_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    with open("images/main_page.jpg", "rb") as img:
        await call.message.answer_photo(photo=img, reply_markup=key.start_key())



@dp.callback_query_handler(Text("profile"))
async def void_callback_query_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    balance = database.get_balance(call["from"]["id"])
    seeds = database.get_seeds(call["from"]["id"])

    text=f"""👨‍🌾 Профиль

🌱 Семена:    {seeds} ед
👛 Баланс:     {balance} TON
"""
    await call.message.answer(text, reply_markup=key.back_key())



@dp.callback_query_handler(Text("buy_seeds"))
async def void_callback_query_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Выберите количество 🌱 семян", reply_markup=key.buy_seeds_key())

@dp.callback_query_handler(Regexp("seed_price="))
async def void_callback_query_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    price = call.data.split("=")[-1].split("_")
    pay_data = await payments.gen_pay_url(price[0])
    keyboard = key.seed_price_key()
    keyboard.add(*[
        types.InlineKeyboardButton("Оплатить", url=pay_data[0]),
        types.InlineKeyboardButton("Проверить оплату", callback_data=f"check_pay={pay_data[-1]}_{price[-1]}"),
        key.back_button
        ])
    await call.message.answer("Оплатите чек", reply_markup=keyboard)

@dp.callback_query_handler(Regexp("check_pay="))
async def void_callback_query_handler(call: types.CallbackQuery, state: FSMContext):
    pay_data = call.data.split("=")[-1].split("_")
    if await payments.check_pay(pay_data[0]):
        database.add_seeds(call["from"]["id"], pay_data[-1])
        await call.message.delete()
        await call.message.answer("Оплата прошла успешно, семена уже доставлены", reply_markup=key.start_key())
    else:
        await call.answer("Вы еще не оплатили чек!", show_alert=True)



@dp.callback_query_handler(Text("withdraw"))
async def void_callback_query_handler(call: types.CallbackQuery, state: FSMContext):
    balance = database.get_balance(call["from"]["id"])
    if balance > 0: 
        if not database.check_balance_withdrawal(call["from"]["id"]):
            await call.answer("Вы уже заказали вывод, ожидате решения по прошлому выводу", show_alert=True)
            return None
        await state.set_state(st.withdraw.count)
        await state.update_data(balance = balance)
        await call.message.delete()
        mes_on_del = await call.message.answer(f"Введите кошелек, на который хотите вывести {balance} TON", reply_markup=key.back_key())
        await state.update_data(mes_on_del=mes_on_del)
    else:
        await call.answer("У вас нет средств, готовых к выводу", show_alert=True)
        
@dp.message_handler(state=st.withdraw.count)
async def start_message_handler(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await data["mes_on_del"].delete()
    balance = data["balance"]
    await state.update_data(count = message.text)
    await message.answer(f"Вы запрашиваете вывод {balance} TON на кошелек {message.text}", reply_markup=key.withdraw_pruf_key())

@dp.callback_query_handler(Text("withdraw_pruf"), state=st.withdraw.count)
async def void_callback_query_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()
    await state.finish()
    await bot.send_message(ADMIN_CHAT,
                           text=f"""Пользователь: {call["from"]["id"]}
Кошелек: `{data["count"]}`
Сумма: `{data["balance"]}`""",
                            parse_mode="MARKDOWN",
                            reply_markup=admin_key.withdraw_admin_key(call["from"]["id"]))
    database.reset_balance(call["from"]["id"])
    await call.message.answer("Админимтратор полуил ваш запрос на вывод, ожидайте", reply_markup=key.start_key())

# @dp.callback_query_handler()
# async def void_callback_query_handler(call: types.CallbackQuery, state: FSMContext):
#     await call.answer()
#     await call.message.delete()
#     await call.message.answer("in dev!!!")