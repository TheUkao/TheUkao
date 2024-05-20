from aiogram import types

def withdraw_admin_key(user_id):
    key=types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton("Оплачено", callback_data=f"withdraw_payment={user_id}"))
    key.add(types.InlineKeyboardButton("Отклонено", callback_data=f"withdraw_unpayment={user_id}"))
    return key