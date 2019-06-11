import telebot
from time import gmtime, strftime, sleep
from sheet import Sheet
from telebot import types
import database_interface
import logging


logging.basicConfig(filename='logging', level=logging.DEBUG)

f = open("token", 'r')

bot = telebot.TeleBot(f.readline())

f.close()



@bot.message_handler(func=lambda message: message.chat.id == message.from_user.id,commands=['start'])
def send_start(message):
    user_id = str(message.chat.id)
    if database_interface.check_vote(user_id, 1) is None:
        if database_interface.new_user(user_id) is False:
            bot.send_message(message.chat.id, "Сталась помилка, спробуй ще раз - /start")
            return
        bot.send_message(message.chat.id, "Привіт, голосуй")
        bot.send_message(message.chat.id, "Проголосуйте за 1 місце:", reply_markup=create_vote_markup(user_id, '1'))
        bot.send_message(message.chat.id, "Проголосуйте за 2 місце:", reply_markup=create_vote_markup(user_id, '2'))
        bot.send_message(message.chat.id, "Проголосуйте за 3 місце:", reply_markup=create_vote_markup(user_id, '3'))
    else:
        bot.send_message(message.chat.id, "Вибери свого фаворита вище")


def create_vote_markup(user_id, place):
    sheet = Sheet("photos_vote_bot")
    participants = sheet.get_participants()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(participants)):
        markup.add(types.InlineKeyboardButton(  text=participants[i],
                                                callback_data=str(user_id) + ';' + place +';' + str(i + 1) + ';' + participants[i]))
    return markup



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    data = call.data.split(';')
    try:
        if data[0] == 'change':
            bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Проголосуйте за " + data[1] + ' місце',
                              reply_markup=create_vote_markup(call.message.chat.id, data[1]))
            #sheet.unvote(int(data[1]), int(data[2]))
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton(text="Змінити вибір", callback_data='change;' + data[1] + ';' + data[2]))
            bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text= "<b>" + data[1] +" місце: </b>" + data[-1],
                              reply_markup=markup,
                              parse_mode='html')
            #sheet.vote(data[0], int(data[1]), int(data[2]))
            database_interface.vote(data[0], int(data[1]), int(data[2]))

    except Exception as msg:
        f = open('errors', 'a+')
        f.write(strftime("[%a, %d %b %Y %H:%M:%S]", gmtime(2)) + ': markup errors: ' + str(msg) + '\n')
        f.close()

@bot.message_handler(commands=['result'])
def result(message):
    sheet = Sheet("photos_vote_bot")
    f = open('admin')
    admins = f.read().splitlines()
    f.close()
    if str(message.chat.id) in admins:
        if database_interface.count_votes(sheet) is True:
            bot.send_message(message.chat.id, "Таблиця результатів оновлена.")
        else:
            bot.send_message(message.chat.id, "Щось пішло не так, спробуй ще раз або напиши розробнику.")
    else:
        bot.send_message(message.chat.id, "Упс... Схоже тебе немає в списку адміністраторів, звернись до розробника.")


while True:
    try:
        bot.infinity_polling(True)
        bot.polling(none_stop=True)

    # ConnectionError and ReadTimeout because of possible timout of the requests library
    # TypeError for moviepy errors
    # maybe there are others, therefore Exception
    except Exception as e:
        f = open('errors', 'a+')
        f.write(strftime("[%a, %d %b %Y %H:%M:%S]", gmtime(2)) + ' Error: ' + str(e) + '\n')
        f.close()