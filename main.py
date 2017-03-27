import telebot
from UserInterface import UIController
#TOKEN : 351825772:AAFhmpdqSYXor4ohuX2UaqDZOLAvHUUFrqw
token = '351825772:AAFhmpdqSYXor4ohuX2UaqDZOLAvHUUFrqw'

bot = telebot.TeleBot(token)

controller = UIController(bot, 'menu.yaml')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global controller
    controller.process_message(message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global controller
    controller.process_message(message)


@bot.callback_query_handler(func=lambda call: True)
def callbeck_test(query):
    global controller
    if query.message:
        controller.process_message(None, query)


bot.polling()