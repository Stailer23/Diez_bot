from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
from dbase_bot import database
import random

class FsmOtz(StatesGroup):
    store = State()
    scrin_otz = State()
    scrin_lk = State()
    # bilet = State()

def gen_billet():
    b=''
    for i in range(6):
        a = str(random.randint(0,9))
        b+=a
    result = int(b)
    return result

def chek_scrin(scrin_list, scrin_id):
    if scrin_id in scrin_list:
        return True
    return False

# @dp.message_handlers(lambda message: 'отзыв' in message.text, state=None)
async def set_store(message: types.Message):
    if await database.check_user(message.chat.id) == False:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Регистрация')).add(
        KeyboardButton('Отмена'))
        await message.answer('Для отправки отзывов необходимо зарегистрироваться!', reply_markup=keyboard)
        return
    await FsmOtz.store.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Озон')).add(
    KeyboardButton('Али'))
    await message.answer('Выберите площадку', reply_markup=keyboard)

async def load_store(message: types.Message, state: FSMContext):
    if message.text != 'Озон' and message.text != 'Али':
        await message.answer('Выберите площадку кнопками')
        return
    async with state.proxy() as data:
        data['store'] = message.text
    await FsmOtz.next()
    await message.reply('Окей! Загрузите скрин отзыва', reply_markup=ReplyKeyboardRemove())

async def load_otziv(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.media_group_id != None:
            await message.reply('Отправьте один скриншот отзыва!')
            await message.delete()
            return
        print(message.photo[0])
        scrin_list = await database.get_scrin_list()
        if chek_scrin(scrin_list, message.photo[0].file_unique_id) == True:
            await message.answer('Вы уже добавляли этот скриншот! Добавьте новый отзыв!')
            await message.delete()
            return
        print(scrin_list)
        data['otziv'] = message.photo[0].file_id
        data['otziv_id'] = message.photo[0].file_unique_id

    await FsmOtz.next()
    await message.reply('Супер! Осталось загрузить скрин лк')

async def load_lk(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.media_group_id != None:
            print(message)
            await message.delete()
            await message.reply('Отправьте только один скриншот ЛК!')
            return
        data['scrin_lk'] = message.photo[0].file_id
        data['lk_id'] = message.photo[0].file_unique_id
    async with state.proxy() as data:
        bil = gen_billet()
        await database.add_comment(message.chat.id, data['store'], data['otziv'], data['scrin_lk'],
                                   data['otziv_id'], data['lk_id'], bil)
        print(data)
    # await FsmOtz.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить еще один отзыв')).add(
    KeyboardButton('Посмотреть мои билеты'))
    await message.reply(f'Отзыв отправлен успешно! номер вашего билета: {bil}\n'
                        f'Подписывайтесь на нашу группу, чтобы не пропутить розыгрыш!\n'
                        f'https://t.me/autopolus', reply_markup=keyboard)
    await state.finish()





def register_handlers_otziv(dp: Dispatcher):
    dp.register_message_handler(set_store, lambda message: 'отзыв' in message.text, state=None)
    dp.register_message_handler(set_store, commands='send_comment', state=None)
    dp.register_message_handler(load_store, state=FsmOtz.store)
    dp.register_message_handler(load_otziv,content_types=['photo'], state=FsmOtz.scrin_otz)
    dp.register_message_handler(load_lk,content_types=['photo'], state=FsmOtz.scrin_lk)

