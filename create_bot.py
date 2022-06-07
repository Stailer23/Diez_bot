from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

storage = MemoryStorage()
bot = Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher(bot, storage=storage)


