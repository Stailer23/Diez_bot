from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
from dbase_bot import database
from aiogram.dispatcher.filters import Text

class FsmPrizes(StatesGroup):
    prizes = State()

async def prizes(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Ежемесячные призы!')).add(
    KeyboardButton('Годовые призы!'))
    await FsmPrizes.prizes.set()
    await message.answer('Мы разыгрываем призы каждый месяц! А также супер-призы среди всех отзывов в конце года!',
                         reply_markup=keyboard)

async def month_prizes(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Годовые призы!')).add(
    KeyboardButton('Отмена'))
    await message.answer('Первый приз: 2000 \u20BD\n'
                         'Второй приз: 1000 \u20BD\n'
                         'Третий приз: 500 \u20BD', reply_markup=keyboard)

async def years_prizes(message: types.Message):
    get_prizes = await database.view_prizes()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Ежемесячные призы!')).add(
    KeyboardButton('Отмена'))
    await message.answer('В конце года разыграем следующие призы:', reply_markup=keyboard)
    for i in get_prizes:
        await message.answer_photo(i["pics"], f'{i["description"]}')


def register_handlers_prizes(dp: Dispatcher):
    dp.register_message_handler(prizes, lambda message: 'Разыгрываемые' in message.text, state=None)
    dp.register_message_handler(prizes, lambda message: 'Разыгрываемые' in message.text, state='*')
    dp.register_message_handler(month_prizes, lambda message: 'Ежемесячные' in message.text, state=FsmPrizes.prizes)
    dp.register_message_handler(years_prizes, lambda message: 'Годовые' in message.text, state=FsmPrizes.prizes)