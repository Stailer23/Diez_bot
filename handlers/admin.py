from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
from dbase_bot import database
from aiogram.dispatcher.filters import Text

class FsmAdmin(StatesGroup):
    spisok = State()
    scrin_otz = State()
    scrin_lk = State()

def check_admin(id_now):
    admins = [621484099, 1220822687]
    if id_now in admins: #Потом поменять на получения списка из бд
        return True
    return False

# @dp.message_handlers(commands='moderator')
async def moder(message: types.Message):
    if check_admin(message.chat.id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Посмотреть список зарезаных')).add(
        KeyboardButton('Какой-то там топ(Нахер этот топ ваще нужен??)'))
        await FsmAdmin.spisok.set()
        await message.answer('Здраствуйте, хозяин, что Вам угодно?', reply_markup=keyboard)
    else:
        # print(message.chat.id)
        await message.answer('Эта команда доступна только Админам.')
    return

async def list_users(message: types.Message):
    get_list = await database.get_list_users()
    cnt=1
    for i, k in get_list.items():
        inline_btn_1 = InlineKeyboardButton(f'Отзывы бедалаги №{cnt}', callback_data=f'button1|{k[1]}')
        inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1)
        cnt_com = await database.cnt_comments(k[1])
        await message.answer(f'Бедалага №{cnt}:\n{i}\nНомер телефона: {k[0]}\nКоличество отзывов: {cnt_com}',reply_markup=inline_kb1)
        cnt+=1
async def call_back(call: types.CallbackQuery):

    a, b = call.data.split('|')
    scrins = await database.get_all_comments(int(b))
    for i in scrins:
        await call.message.answer_photo(i['comment'], 'Отзыв')
        await call.message.answer_photo(i['lk'], 'Личный кабинет')
    # print(scrins)

    return scrins




def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(moder, commands='moderator', state=None)
    dp.register_message_handler(list_users, state=FsmAdmin.spisok)
    dp.register_callback_query_handler(call_back, Text(startswith='button1'), state='*')