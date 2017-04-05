import telebot
from UserInterface import UIController
#TOKEN : 351825772:AAFhmpdqSYXor4ohuX2UaqDZOLAvHUUFrqw
token = '366896647:AAE4slt_CObEA4AQw3Fjty6rkchbAlaEDfU'

bot = telebot.TeleBot(token)

controller = UIController(bot, 'menu.yaml')

from QuestionBotController import Controller
ctrl = Controller()
#ctrl.find_closest_question('')

#exit(0)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global controller, ctrl
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