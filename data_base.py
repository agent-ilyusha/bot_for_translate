# -- coding: utf-8

import sqlite3


def create_db():
    try:

        conn = sqlite3.connect('data_base/usersId_and_languages.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (user_id int PRIMARY KEY , languages txt)")
        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        pass
    finally:
        conn.close()


def insert_table(lang_list: list, id: int):
    try:

        conn = sqlite3.connect('data_base/usersId_and_languages.db')
        cursor = conn.cursor()
        lang_str = ' '.join(lang_list)
        varib = (id, lang_str)

        cursor.execute("INSERT INTO users (user_id, languages) VALUES (?, ?)", varib)
        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print(error)
    finally:
        conn.close()


def update_table(lang_list: list, id: int):
    try:

        conn = sqlite3.connect('data_base/usersId_and_languages.db')
        cursor = conn.cursor()
        lang_str = ' '.join(lang_list)
        varib = (lang_str, id)

        cursor.execute("UPDATE users SET languages = ? WHERE user_id = ?", varib)
        conn.commit()

    except sqlite3.Error as error:
        print(error)
    finally:
        conn.close()


def return_language(id: int) -> list:
    try:

        conn = sqlite3.connect('data_base/usersId_and_languages.db')
        cursor = conn.cursor()
        varib = (id, )
        cursor.execute("SELECT languages FROM users WHERE user_id = ?", varib)
        conn.commit()
        varib = cursor.fetchall()[0][0]
        return varib.split()

    except sqlite3.Error as error:
        print(error)
    finally:
        conn.close()


def return_users():
    try:
        conn = sqlite3.connect('data_base/usersId_and_languages.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        conn.commit()
        varib = list(el for varib in cursor.fetchall() for el in varib)  # перебор пользователей
        return varib
    except sqlite3.Error as error:
        print(error)
    finally:
        conn.close()




'''
create_db - создает базу данных. ничего не принимает.
insert_table - добавляет в базу данных пользователя и дефолтные языки. принимает список языков и id пользователя.
update_table - обновляет в базе данных язык. принимает список языков и id пользователя.
return_language - возвращает список языков пользователя. принимает id пользователя.
return_users - возвращает id всех пользователей. ничего не принимает.
'''
