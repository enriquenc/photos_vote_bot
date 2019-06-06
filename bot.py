import telebot
from sheet import Sheet


f = open("token", 'r')

bot = telebot.TeleBot(f.readline())

f.close()

sheet = Sheet("photos_vote_bot")

@bot.message_handler(func=lambda message: message.chat.id == message.from_user.id,commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, "Привіт, голосуй")
    msg = ''
    p = sheet.get_participants()
    for element in p:
        msg = msg + str(p.index(element) + 1) + '. ' + element + '\n'
    bot.send_message(message.chat.id, msg)


bot.polling()