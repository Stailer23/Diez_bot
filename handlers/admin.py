from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
from dbase_bot import database
from aiogram.dispatcher.filters import Text
from datetime import datetime

class FsmAdmin(StatesGroup):
    spisok = State()
    scrin_otz = State()
    scrin_lk = State()
    prizes = State()
    add_photo_prize = State()
    add_description_prize = State()

def check_admin(id_now):
    admins = [621484099, 1220822687]
    if id_now in admins: #Потом поменять на получения списка из бд
        return True
    return False

# @dp.message_handlers(commands='moderator')
async def moder(message: types.Message, state: FSMContext):
    if check_admin(message.chat.id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Посмотреть список зареганых')).add(
        KeyboardButton('Отзывы за текущий месяц')).add(
        KeyboardButton('Редактор призов')).add(
    KeyboardButton('Отмена'))
        current_sate = await state.get_state()
        if current_sate != None:
            await state.finish()
        # await state.finish()
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
    await call.message.answer("Все отзывы бедалаги:")
    for i in scrins:
        await call.message.answer_photo(i['comment'], f'Билет № {i["billet"]}\n'
                                                      f'Площадка: {i["store"]}\n'
                                                      f'Дата: {i["date"]}')
        await call.message.answer_photo(i['lk'], 'Личный кабинет')
    return scrins

async def view_com_month(message: types.Message):
    get_com = await database.get_commets_month(datetime.strftime(datetime.now(),' %m'))
    cnt = 1
    for i in get_com:
        inline_btn_2 = InlineKeyboardButton(f'Автор коммента №{cnt}', callback_data=f'button2|{i["user_id"]}')
        inline_kb2 = types.InlineKeyboardMarkup().add(inline_btn_2)
        await message.answer_photo(i['comment'], f'Коммент № {cnt}\n'
                                                 f'Билет № {i["billet"]}\n'
                                                 f'Площадка: {i["store"]}\n'
                                                 f'Дата отправки: {i["date"]}', reply_markup=inline_kb2)
        cnt+=1


async def one_user(call: types.CallbackQuery):
    a, b = call.data.split('|')
    get_user = await database.get_user(int(b))
    inline_btn_1 = InlineKeyboardButton(f'Отзывы автора {get_user["name"]}', callback_data=f'button1|{int(b)}')
    inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1)
    cnt_com = await database.cnt_comments(int(b))
    await call.message.answer(f'{get_user["name"]}\nНомер телефона: {get_user["phone"]}\nКоличество отзывов: {cnt_com}',
                         reply_markup=inline_kb1)

async def view_prize_list(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Добавить приз')).add(
    KeyboardButton('Отмена'))
    get_prizes = await database.view_prizes()
    await FsmAdmin.prizes.set()
    if get_prizes == []:
        # await FsmAdmin.prizes.set()
        await message.answer('Призов еще нет. Добавьте.', reply_markup=keyboard)
    else:

        await message.answer('Вот текущие призы:', reply_markup=keyboard)
        for i in get_prizes:
            inline_btn_del = InlineKeyboardButton(f'Удалить', callback_data=f'buttondel|{i["id"]}')
            inline_kb_del = types.InlineKeyboardMarkup().add(inline_btn_del)
            await message.answer_photo(i["pics"],f'{i["description"]}',reply_markup=inline_kb_del)


async def add_prize(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отмена'))
    await FsmAdmin.add_photo_prize.set()
    await message.answer("Добавь картинку подарка", reply_markup=keyboard)

async def load_pic_prize(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отмена'))
    async with state.proxy() as data:
        if message.media_group_id != None:
            await message.reply('Отправьте один скриншот подарка!')
            await message.delete()
            return
        data['pic'] = message.photo[0].file_id
    await FsmAdmin.add_description_prize.set()
    await message.reply('Теперь добавь описание приза', reply_markup=keyboard)

async def load_description_prize(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    async with state.proxy() as data:
        await database.add_prize(data["pic"], data["description"])
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Добавить еще один приз')).add(
    KeyboardButton('Посмотреть список призов')).add(
    KeyboardButton('Отмена'))
    await FsmAdmin.prizes.set()
    await message.answer('Приз добавлен!', reply_markup=keyboard)

async def delete_prize(call: types.CallbackQuery):
    a, b = call.data.split('|')
    await database.del_prize(int(b))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Добавить приз')).add(
    KeyboardButton('Обновить список призов')).add(
    KeyboardButton('Отмена'))
    await call.message.answer('Приз удален!', reply_markup=keyboard)




def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(moder, commands='moderator', state=None)
    dp.register_message_handler(moder, commands='moderator', state='*')
    dp.register_message_handler(list_users,lambda message: 'зареганых' in message.text, state=FsmAdmin.spisok)
    dp.register_callback_query_handler(call_back, Text(startswith='button1'), state='*')
    dp.register_callback_query_handler(one_user, Text(startswith='button2'), state='*')
    dp.register_message_handler(view_com_month, lambda message: 'текущий' in message.text, state=FsmAdmin.spisok)
    dp.register_message_handler(view_prize_list, lambda message: 'Редактор' in message.text, state=FsmAdmin.spisok)
    dp.register_message_handler(view_prize_list, lambda message: 'список призов' in message.text, state='*')
    dp.register_message_handler(add_prize, lambda message: 'Добавить' in message.text, state=FsmAdmin.prizes)
    dp.register_message_handler(load_pic_prize, content_types=['photo'], state=FsmAdmin.add_photo_prize)
    dp.register_message_handler(load_description_prize, state=FsmAdmin.add_description_prize)
    dp.register_callback_query_handler(delete_prize, Text(startswith='buttondel'), state=FsmAdmin.prizes)