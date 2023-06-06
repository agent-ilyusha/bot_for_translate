# -- coding: utf-8
import telebot as tl
from telebot import types
import translate
import data_base
import speech
import audio_file
from os import path
import json

with open('C:\\Users\\1\\Desktop\\tokens\\tokens.json', 'r') as file:
    TOKEN = json.load(file)['token_bot_translate']  # токен

bot = tl.TeleBot(f'{TOKEN}')
list_language = ['русский', 'испанский', 'немецкий', 'английский', 'корейский', ]  # дефолтный список языков
language_change = 0
key_lang = 0
frog_stick = open('C:/Users/1/Desktop/new_bot/stiker/Frog.tgs', 'rb')

try:
    def db_func(message, list_language_user, user_id):
        del list_language_user[0]
        list_language_user.append(message.text.lower())  # добавление последнего использованного языка пользователя в конец списка
        data_base.update_table(list_language_user, user_id)  # обновление sql


    def choice_language(message):
        global key_lang

        llist_but = list()
        markup = types.ReplyKeyboardMarkup(True, False)
        language = data_base.return_language(message.chat.id)

        for i in range(5):
            but = types.KeyboardButton(text=language[i])
            llist_but.append(but)
        markup.add(*llist_but)

        key_lang = translate.give_key_lang(message.text)

        # проверка на ошибку с выбором языка
        if key_lang == 0:
            bot.send_message(message.chat.id, 'Попробуй снова выбрать язык!', reply_markup=markup)
        else:
            if message.text.lower() not in language:  # проверка на наличие языка в списке языков пользователя, если его нет, то язык будет добавлен в список
                print(3)
                db_func(message, data_base.return_language(message.chat.id), message.chat.id)
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Введите текст', reply_markup=markup)
            bot.register_next_step_handler(message, translate_func)


    def translate_func(message):
        global key_lang
        llist_but = list()
        markup = types.ReplyKeyboardMarkup(True, False)
        trans = translate.process_func(message.text, key_lang)
        bot.send_message(message.chat.id, trans, reply_markup=markup)
        # цикл нужен для добавления кнопок с языком
        for i in ('/голосовое', '/текст'):
            but = types.KeyboardButton(i)
            llist_but.append(but)
        markup.add(*llist_but)
        bot.send_message(message.chat.id,
                         '''СПИСОК КОММАНД: /stop - для остановки бота /start - для перезапуска бота. P.S. Голосовые функции доступны, но работают плохо!''')
        bot.send_message(message.chat.id,
                         'Выбери тип сообщения!',
                         reply_markup=markup)


    def audio_func(message):
        global list_language
        llist_but = list()

        fileid = bot.get_file(file_id=message.voice.file_id)
        file_down = bot.download_file(fileid.file_path)
        path_ogg = path.join('C:\\Users\\1\\Desktop\\new_bot\\audio\\' + fileid.file_unique_id + '.ogg')

        with open(path_ogg, 'wb') as file:
            file.write(file_down)

        path_wav = audio_file.func_soundFile(path_ogg)
        txt = speech.func_speech(path_wav)
        file_path = audio_file.func_gtts(txt, path_wav)

        bot.send_message(message.chat.id, text=txt)
        with open(file_path, 'rb') as file:
            bot.send_voice(message.chat.id, file)

        markup = types.ReplyKeyboardMarkup(True, False)
        # цикл нужен для добавления кнопок с языком
        for i in ('/голосовое', '/текст'):
            but = types.KeyboardButton(i)
            llist_but.append(but)
        markup.add(*llist_but)
        bot.send_message(message.chat.id,
                         '''СПИСОК КОММАНД: /stop - для остановки бота /start - для перезапуска бота''')
        bot.send_message(message.chat.id,
                         'Выбери тип сообщения!',
                         reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def welcome_message(message):
        global list_language
        llist_but = list()
        markup = types.ReplyKeyboardMarkup(True, False)
        # цикл нужен для добавления кнопок с языком
        for i in ('/голосовое', '/текст'):
            but = types.KeyboardButton(i)
            llist_but.append(but)
        markup.add(*llist_but)
        bot.send_message(message.chat.id,
                         'Привет, выбери тип сообщения!',
                         reply_markup=markup)

    @bot.message_handler(commands=['голосовое'])
    def choice_audio(message):
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Отправь голосовое сообщение', reply_markup=markup)
        bot.register_next_step_handler(message, audio_func)


    @bot.message_handler(commands=['stop'])
    def stop_func(message):
        global frog_stick
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Пока друг', reply_markup=markup)
        bot.send_sticker(message.chat.id, frog_stick)



    @bot.message_handler(commands=['текст'])
    def choice_text(message):
        global key_lang

        llist_but = list()
        list_users_id = data_base.return_users()

        if message.chat.id not in list_users_id:  # проверяется, есть ли в sql пользователь с таким id
            data_base.insert_table(list_language, message.chat.id)

        markup = types.ReplyKeyboardMarkup(True, False)
        language = data_base.return_language(message.chat.id)

        for i in range(5):
            but = types.KeyboardButton(text=language[i])
            llist_but.append(but)

        markup.add(*llist_but)

        bot.send_message(message.chat.id, 'Выбери язык!', reply_markup=markup)
        bot.register_next_step_handler(message, choice_language)





except:
    @bot.message_handler(content_types=['text'])
    def error(message):
        bot.send_message(message.chat.id, 'Упс, произошла непредвиденная ошибка. Попробуйте еще раз!')
finally:
    bot.polling()

'''
db_func - добавляет последний использованный язык пользователя в sql. принимает в виде параметров сообщение пользователя, список языков пользователя и id пользователя.
welcome_message - нужна для запуска бота, запускается по команде /start. принимает сообщение.
stop_func - нужна для остановки бота у пользователя, запускается по команде /stop. принимает сообщение.
choice_language - с помощью этой функции происходит выбор языка. принимает сообщение.
translate_func - в этой функции происходит перевод текста. принимает сообщение.
error - нужна, если произойдет ошибка. принимает сообщение.
'''

