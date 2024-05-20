from aiogram import types

back_button = types.InlineKeyboardButton("Назад", callback_data="back_main_menu")

def back_key():
    key = types.InlineKeyboardMarkup()
    key.row(back_button)
    return key


def start_key():
    key = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton("👨‍🌾 Профиль", callback_data="profile")]
    key.row(*buttons)
    buttons = [types.InlineKeyboardButton("🌱 Фарм", callback_data="buy_seeds")]
    key.row(*buttons)
    buttons = [types.InlineKeyboardButton("📤 Вывести", callback_data="withdraw")]
    key.row(*buttons)
    return key

def buy_seeds_key():
    key = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("0.2 TON    /    1 🌱 семечко", callback_data="seed_price=0.2_1"),
        types.InlineKeyboardButton("0.5 TON    /    3 🌱 семечка", callback_data="seed_price=0.5_3"),
        types.InlineKeyboardButton("1 TON    /    7 🌱 семечек", callback_data="seed_price=1_7")
        ]
    key.add(*buttons)
    key.row(back_button)
    return key

def seed_price_key():
    key = types.InlineKeyboardMarkup(row_width=1)
    return key

def withdraw_pruf_key():
    key = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton("Подтвердить", callback_data="withdraw_pruf")]
    key.add(*buttons)
    key.row(back_button)
    return key

