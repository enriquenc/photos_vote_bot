import telebot
from sheet import Sheet
from telebot import types
from database_interface import new_user, check_vote

f = open("token", 'r')

bot = telebot.TeleBot(f.readline())

f.close()

sheet = Sheet("photos_vote_bot")

@bot.message_handler(func=lambda message: message.chat.id == message.from_user.id,commands=['start'])
def send_start(message):
    if check_vote(str(message.chat.id), 1) is None:
        new_user(str(message.chat.id))
        bot.send_message(message.chat.id, "Привіт, голосуй")
        bot.send_message(message.chat.id, "Проголосуйте за 1 місце:", reply_markup=create_vote_markup(message, '1'))
        bot.send_message(message.chat.id, "Проголосуйте за 2 місце:", reply_markup=create_vote_markup(message, '2'))
        bot.send_message(message.chat.id, "Проголосуйте за 3 місце:", reply_markup=create_vote_markup(message, '3'))
    else:
        bot.send_message(message.chat.id, "Вибери свого фаворита вище")


#@bot.message_handler(commands=['vote'])


def create_vote_markup(message, place):
    user_id = str(message.from_user.id)

    participants = sheet.get_participants()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(participants)):
        markup.add(types.InlineKeyboardButton(  text=participants[i],
                                                callback_data=user_id + ';' + place +';' + str(i + 1) + ';' + participants[i]))
    return markup



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    data = call.data.split(';')

    if data[0] == 'change':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Проголосуйте за " + data[1] + ' місце',
                              reply_markup=create_vote_markup(call.message, data[1]))
        sheet.unvote(int(data[1]), int(data[2]))
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(text="Змінити вибір", callback_data='change;' + data[1] + ';' + data[2]))
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text= "<b>" + data[1] +" місце: </b>" + data[-1],
                              reply_markup=markup,
                              parse_mode='html')
        sheet.vote(data[0], int(data[1]), int(data[2]))


@bot.message_handler(command=['null'])
def null(message):
    sheet.null()


bot.polling()