from aiogram import executor, types
import asyncio
from dbase_bot.database import DataBase
# from aiogram.methods import SendPhoto

from create_bot import dp
from aiogram.types import KeyboardButton, BotCommand

async def on_startup(_):
    print('Бот запущен')

@dp.message_handler(commands=['start','help'])
async def start_bot(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Регистрация'))
    await message.answer('Привет! Я бот, создан для того, чтобы Вячеслав кого-то наебал! '
                         'или поднял кучу бабла. Но это не мое дело. Моё дело - выдать '
                         'Вам выйгрышный билетик в обмен на скрин с Озона или Али. Давайте для начала '
                         'зарегистрируемся, чтобы мы могли с вами связаться в случае выйгрыша! '
                         'Нажмите кнопку "Регистрация" внизу экрана.', reply_markup=keyboard)



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
