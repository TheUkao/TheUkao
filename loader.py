from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN

bot = Bot(6850164038:AAG7fKbZXlWlpyaP0LJR1HzhEqgs3V1diE0)
dp = Dispatcher(bot, storage=MemoryStorage())