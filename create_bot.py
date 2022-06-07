from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

storage = MemoryStorage()
bot = Bot(token=os.environ.get('TOKEN'))
# bot = Bot(token='5515165760:AAE6Of-wXLuOfYNw7xeSuEfVjWP07sEV38w')
dp = Dispatcher(bot, storage=storage)


