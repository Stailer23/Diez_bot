from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from dbase_bot.database import DBcomm, DataBase, reg_user
from dbase_bot import database
from datetime import datetime

class FsmReg(StatesGroup):
    name = State()
    cont = State()

# @dp.message_handlers(commands='q', state=None)
async def cm_start(message: types.Message):
    if await database.check_user(message.chat.id) == True:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отправить отзыв')).add(
        KeyboardButton('Посмотреть мои билеты')).add(
        KeyboardButton('Разыгрываемые призы'))
        await message.answer('Вы уже зарегистированы! Добавляйте отзывы и получайте билеты!', reply_markup=keyboard)
        return
    await FsmReg.name.set()
    await message.answer('Введите фио', reply_markup=ReplyKeyboardRemove())

async def cancel(message: types.Message, state: FSMContext):
    current_sate = await state.get_state()
    if current_sate == None:
        return
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Регистрация')).add(
    KeyboardButton('Отправить отзыв')).add(
    KeyboardButton('Посмотреть мои билеты')).add(
    KeyboardButton('Разыгрываемые призы'))
    await message.answer('Ок! Текущее действие отменено', reply_markup=keyboard)

# @dp.message_handlers(state=FsmReg.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.text.isdigit() or len(message.text)<5:
        keyboard_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отмена'))
        await message.answer('Что-то не похоже на ФИО, попробуйте еще раз', reply_markup=keyboard_cancel)
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await FsmReg.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Поделиться контактом!', request_contact=True))
    await message.answer('Супер! Отправьте свой контакт!', reply_markup=keyboard)

# @dp.message_handlers(content_types=['contact'], state=FsmReg.cont)
async def load_cont(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
    async with state.proxy()as data:
        # dbase = DBcomm()
        await reg_user(message.chat.id, data['name'], data['phone'], datetime.now())
        # print(data)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить отзыв')).add(
    KeyboardButton('Посмотреть мои билеты')).add(
    KeyboardButton('Разыгрываемые призы'))
    await message.answer('Регистрация завершена! Отправьте свой первый отзыв!', reply_markup=keyboard)
    await state.finish()

def register_handlers_reg(dp: Dispatcher):
    dp.register_message_handler(cm_start, lambda message: 'Регистрация' in message.text, state=None)
    dp.register_message_handler(cm_start, commands='register', state=None)
    dp.register_message_handler(cancel, commands='cancel', state='*')
    dp.register_message_handler(cancel, lambda message: 'Отмена' in message.text, state='*')
    dp.register_message_handler(load_name, state=FsmReg.name)
    dp.register_message_handler(load_cont, content_types=['contact'], state=FsmReg.cont)