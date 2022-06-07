from dbase_bot import database
from aiogram import types, Dispatcher
from aiogram.types import KeyboardButton


async def view_bil(message: types.Message):
    if await database.check_user(message.chat.id) == False:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Регистрация')).add(
            KeyboardButton('Отправить отзыв')).add(
        KeyboardButton('Отмена'))
        await message.answer('У вас пока нет билетов. Для полчения необходимо зарегистрироваться и отправить отзыв!', reply_markup=keyboard)
        return
    billet_list = await database.view_billets(message.chat.id)
    if billet_list == []:
        await message.answer('У вас пока нет билетов. Отправьте отзыв для получения.', reply_markup=keyboard)
    await message.answer('Список Ваших билетов:')
    for i in billet_list:
        await message.answer(i)

def register_handlers_billets(dp: Dispatcher):
    dp.register_message_handler(view_bil, lambda message: 'билеты' in message.text)