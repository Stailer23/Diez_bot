from typing import Union
import asyncpg, os
from asyncpg import Connection, exceptions
from asyncpg.pool import Pool
import ssl
from datetime import datetime
ssl_object = ssl.create_default_context()
ssl_object.check_hostname = False
ssl_object.verify_mode = ssl.CERT_NONE

class DBcomm:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create_pool(self):
        # self.pool = await asyncpg.create_pool(database="db_bot", user="postgres", password="153789", host="127.0.0.1",
        #                              port="5432")
        self.pool = await asyncpg.create_pool(dsn=os.environ.get('DATABASE_URL'), ssl=ssl_object)


    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
        return result
DataBase = DBcomm()

async def reg_user(id_tlgrm, user_name, contact, date, DataBase=DataBase):
    sql = """INSERT INTO users (user_id, name, phone, date) VALUES ($1, $2, $3, $4)"""
    await DataBase.execute(sql, id_tlgrm, user_name, contact, date, execute=True)

async def check_user(id_tlgrm):
    sql = '''SELECT id FROM users WHERE user_id = $1'''
    result = await DataBase.execute(sql, id_tlgrm, fetch=True)
    if result == []:
        return False
    return True

async def add_comment(id_tlgrm, store, comment, lk, com_id, lk_id, billet, date, DataBase=DataBase):
    sql = '''INSERT INTO comments (user_id, store, comment, lk,com_id, lk_id, billet, date) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)'''
    await DataBase.execute(sql, id_tlgrm, store, comment, lk, com_id, lk_id, billet, date, execute=True)


async def view_billets(id_tlgrm, DataBase=DataBase):
    sql = '''SELECT billet FROM comments WHERE user_id = $1'''
    values = await DataBase.execute(sql, id_tlgrm, fetch=True)
    data = []
    for i in values:
        data.append(i['billet'])
    return data

async def get_scrin_list(DataBase=DataBase):
    sql = '''SELECT com_id, lk_id FROM comments'''
    values = await DataBase.execute(sql, fetch=True)
    data = []
    for i in values:
        data.append(i['com_id'])
        data.append(i['lk_id'])
    return data

async def get_list_users(DataBase=DataBase):
    sql = '''SELECT users.name, users.phone, users.user_id FROM users       
             '''
    values = await DataBase.execute(sql, fetch=True)
    data = dict()
    for i in values:
        a = [i['phone'], i['user_id']]
        data[i['name']] = a
    return data

async def get_user(id_tlgrm, DataBase=DataBase):
    sql = '''SELECT name, phone FROM users WHERE user_id = $1'''
    values = await DataBase.execute(sql, id_tlgrm, fetchrow=True)
    return values

async def cnt_comments(id_tlgrm, DataBase=DataBase):
    sql = """SELECT COUNT(comment) FROM comments WHERE user_id = $1"""
    values = await DataBase.execute(sql, id_tlgrm, fetch=True)
    data = []
    for i in values:
        data.append(i['count'])
    data = int(*data)
    return data

async def get_all_comments(id_tlgrm, DataBase=DataBase):
    sql = '''SELECT comment, lk, billet, store, date FROM comments WHERE user_id = $1'''
    values = await DataBase.execute(sql, id_tlgrm, fetch=True)
    data = []
    for i in values:
        data_dict=dict()
        data_dict['billet'] = i['billet']
        data_dict['store'] = i['store']
        data_dict['comment'] = i['comment']
        data_dict['lk'] = i['lk']
        data_dict['date'] = datetime.strftime(i['date'], '%d/%m/%y')
        data.append(data_dict)
    return data

async def get_commets_month(month, DateBase = DataBase):
    sql = '''SELECT user_id, store, comment, billet, date FROM comments WHERE EXTRACT(MONTH FROM date) = $1'''
    values = await DataBase.execute(sql, month, fetch=True)
    a = []
    b=[]
    for i in values:
        a.append(i)
    for k in a:
        data = dict()
        data['user_id'] = k[0]
        data['store'] = k[1]
        data['comment'] = k[2]
        data['billet'] = k[3]
        data['date'] = datetime.strftime(k[4],'%d/%m/%y')
        b.append(data)
    # print(b)
    return b

async def view_prizes(DataBase=DataBase):
    sql = '''SELECT * FROM prizes'''
    values = await DataBase.execute(sql, fetch=True)
    return values

async def edit_prizes(id, DataBase=DataBase):
    pass

async def add_prize(pics, description, DataBase=DataBase):
    sql = '''INSERT INTO prizes (pics, description) VALUES ($1, $2)'''
    try:
        await DataBase.execute(sql, pics, description, execute=True)
    except asyncpg.ForeignKeyViolationError as e:
        print('Ошибка при работе с БД', e)


async def del_prize(id, DataBase=DataBase):
    sql = '''DELETE FROM prizes WHERE id = $1'''
    await DataBase.execute(sql, id, execute=True)