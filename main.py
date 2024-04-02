import telebot
from telebot import types
from config import BOT_TOKEN
import api
import database

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f'{message.chat.first_name}, здраствуйте! Я бот Яндекс-словаря, сейчас я расскажу вам что я умею\n\n'
                     f'Моя основная функция это переводить слова\n'
                     f'для начала работы выберите язык перевода отправив /lang \n'
                     f'для получения списка команд /help')
    database.user_reg(message.from_user.id)
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Список команд бота:\n'
                                      '/start - начало работы и регистрация пользователя в боте\n'
                                      '/lang - добавить язык перевода\n'
                                      '/delite - удалить язык перевода\n')

@bot.message_handler(commands=['lang'])
def select_lang(message):
    bot.send_message(message.chat.id, 'Введите язык перевода из списка в следущем сообщении и напишите его в чат (к примеру: ru-en)\n{api.get_langs()}')
    bot.register_next_step_handler(message, add_lang)

def add_lang(message):
    lang = message.text.rstrip().lower()
    if lang in api.get_langs():
        database.add_lang(message.from_user.id, lang)
        bot.send_message(message.chat.id, 'Язык перевода добавлен, для продолжения работы напишите слово которое хотите перевести')
    else:
        bot.send_message(message.chat.id, 'Неверно введен язык перевода, повторите попытку\n'
                                          '(Сообщение должно выглядить так: ru-en)')
        bot.register_next_step_handler(message, add_lang)

@bot.message_handler(commands=['delete'])
def start_delete(message):
    langs = database.get_langs(message.from_user.id)
    if None not in langs:
        bot.send_message(message.chat.id, 'Напишите пару языков которые вы хотите удалить\n'
                                          '(Пример текста сообщения: ru-en)')
        bot.register_next_step_handler(message, delete)
    else:
        bot.send_message(message.chat.id, "Вы еще не выбрпли язык для перевода")


def delete(message):
    delete_elem = message.text.rstrip().lower()
    langs = database.get_langs(message.from_user.id)
    if delete_elem in langs[0]:
        langs = langs[0].split()
        langs.pop(langs.index(delete_elem))
        langs = set(langs)
        new_langs = ' '.join(langs)
        database.delete(new_langs, message.from_user.id)
        bot.send_message(message.chat.id, 'Язык перевода удален, для продолжения работы напишите слово которое хотите перевести')
    else:
        bot.send_message(message.chat.id, 'Такой языковой пары нет в вашем наборе языков или Вы неправильно ввели сообщение')


@bot.message_handler(content_types=['text'])
def translation(message):
    markup = types.InlineKeyboardMarkup()
    langs = set(database.get_langs(message.from_user.id)[0].split())
    for lang in langs:
        button = types.InlineKeyboardButton(f'{lang}', callback_data=f'{lang}')
        markup.add(button)
    bot.reply_to(message, message.text, reply_markup=markup)
    if None in langs:
        bot.send_message(message.chat.id, 'Вы еще не выбрали язык для перевода, выберите язык перевода и отправьте слово повторно')


@bot.callback_query_handler(func=lambda call: True)
def callback(callback):
    try:
        bot.send_message(callback.message.chat.id, api.display(api.lookup(callback.data, callback.message.reply_to_message.text)))
    except Exception:
        bot.send_message(callback.message.chat.id, "Такого слова нет в словаре")

bot.polling(none_stop=True)
