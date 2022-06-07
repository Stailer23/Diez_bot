from aiogram import executor, types
import asyncio
from dbase_bot.database import DataBase

from create_bot import dp
from aiogram.types import KeyboardButton, BotCommand

async def on_startup(_):
    print('Бот запущен')


@dp.message_handler(commands=['start','help'])
async def start_bot(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Регистрация'))
    await message.answer('''
    Привет, видимо ты тут чтобы забрать главный приз? Или не главный? 🤔
В общем в любом случае ты зашёл сюда за бонусом и ты его получишь! 🎉
Все что тебе нужно это оставить отзыв и полагаться на фортуну! А она тебе точно благоволит 😉. 
Быстрее регистрируйся и попытай свою удачу а в ежемесячном розыгрыше и годовом супер розыгрыше! Действуй, и удачи тебе! 💪🤝
    ''', reply_markup=keyboard)



from handlers import register, otziv, tg_billets, admin

register.register_handlers_reg(dp)
otziv.register_handlers_otziv(dp)
tg_billets.register_handlers_billets(dp)
admin.register_handlers_admin(dp)
# Установка команд бота


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DataBase.create_pool())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
