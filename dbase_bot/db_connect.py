import psycopg2, os
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_table():
    try:
        # Подключение к существующей базе данных
        # connection = psycopg2.connect(user="postgres",
        #                               # пароль, который указали при установке PostgreSQL
        #                               password="123456",
        #                               host="127.0.0.1",
        #                               port="5432")
        connection = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_create_database = 'create database postgres_db'
        cursor.execute(sql_create_database)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def create_new_table_users():
    try:
        # Подключиться к существующей базе данных
        # connection = psycopg2.connect(user="postgres",
        #                               # пароль, который указали при установке PostgreSQL
        #                               password="153789",
        #                               host="127.0.0.1",
        #                               port="5432",
        #                               database="db_bot")
        connection = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')

        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        create_table_query = '''CREATE TABLE IF NOT EXISTS users
                                  (id SERIAL,
                                  user_id           INTEGER    NOT NULL,
                                  NAME   VARCHAR(100),
                                  PHONE VARCHAR(100),
                                  PRIMARY KEY(user_id)); '''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица users успешно создана в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def create_new_table_comments():
    try:
        # Подключиться к существующей базе данных
        # connection = psycopg2.connect(user="postgres",
        #                               # пароль, который указали при установке PostgreSQL
        #                               password="153789",
        #                               host="127.0.0.1",
        #                               port="5432",
        #                               database="db_bot")
        connection = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')
        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        create_table_query = '''CREATE TABLE IF NOT EXISTS comments
                                  (id SERIAL,
                                  user_id           INTEGER    NOT NULL,
                                  store VARCHAR(50),
                                  comment   VARCHAR(100),
                                  lk VARCHAR(100),
                                  com_id VARCHAR(100),
                                  lk_id VARCHAR (100),
                                  billet INTEGER,                                  
                                  CONSTRAINT fk_users
                                    FOREIGN KEY(user_id) 
                                        REFERENCES users(user_id));'''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица comments успешно создана в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")