from loader import dp 
from aiogram import executor
from aiogram.types import BotCommand
import handlers
from utils.database import open_db, add_balance_by_seeds
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime



async def on_startup(_):
    open_db()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(add_balance_by_seeds, trigger="cron", hour=datetime.now().hour, minute=datetime.now().minute+1, start_date=datetime.now())
    scheduler.start()
    await dp.bot.set_my_commands([
        BotCommand("start", "Запуск / Перезапуск бота")
    ])
    

executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)