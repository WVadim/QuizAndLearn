# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 18:32:13 2017

@author: Javier
"""
import telebot
from telebot import types

bot = telebot.TeleBot("335396227:AAEJ5MWykURPRRFTMNso2NFT90o6Jn93bz8")
requested = None
answering = None
answers=[]
questions=[]
cont=0


@bot.message_handler(commands=[u'start', u'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, u'I\'m a bot, please talk to me!')


@bot.message_handler(commands=[u'pull'])
def pull(message):
    global requested
    global cont
    bot.send_message(message.chat.id, u'You have requested to get quiz answers')
    # Connecting to the database
    # Get themes from connector
    markup = types.ReplyKeyboardMarkup()
    itembtnone = types.KeyboardButton(u'Geography')
    itembtntwo = types.KeyboardButton(u'Entertainment')
    itembtnthree = types.KeyboardButton(u'History')
    itembtnfour = types.KeyboardButton(u'Art & Literature')
    itembtnfive = types.KeyboardButton(u'Science & Nature')
    itembtnsix = types.KeyboardButton(u'Sports & Leisure')
    markup.row(itembtnone, itembtntwo, itembtnthree)
    markup.row(itembtnfour, itembtnfive, itembtnsix)
    bot.send_message(message.chat.id, u'Choose a theme:', reply_markup=markup)
    requested = True
    cont = 0



@bot.message_handler(func=lambda message: True)
def check_answer(message):
    global requested
    global answering
    global questions
    global cont
    global answers
    if (requested):
        if (answering != True):
            # Get random questions of Geography from the connector according to the theme
            if (message.text == u'Geography'):
                questions = [u'What is the capital city of Spain?', u'Another one', u'another one']
                #Send the first question
                q = questions[cont]

                # Query to the connector to get the options to that question
                opts = [u'Valencia', u'Barcelona', u'Madrid', u'Seville']

                bot.send_message(message.chat.id, q)
                markup = types.ReplyKeyboardMarkup()
                itembtnone = types.KeyboardButton(opts[0])
                itembtntwo = types.KeyboardButton(opts[1])
                itembtnthree = types.KeyboardButton(opts[2])
                itembtnfour = types.KeyboardButton(opts[3])
                markup.row(itembtnone, itembtntwo)
                markup.row(itembtnthree, itembtnfour)
                bot.send_message(message.chat.id, u'Choose one option:', reply_markup=markup)
                answering = True
                cont = cont + 1


        else:
            if(cont < 3):
                #Store answer in answers
                answers.insert(cont-1, message.text)
                #next question
                q = questions[cont]

                #Query to the connector to get the options to that question
                opts=[u'Valencia', u'Barcelona', u'Madrid', u'Seville']

                bot.send_message(message.chat.id, q)
                markup = types.ReplyKeyboardMarkup()
                itembtnone = types.KeyboardButton(opts[0])
                itembtntwo = types.KeyboardButton(opts[1])
                itembtnthree = types.KeyboardButton(opts[2])
                itembtnfour = types.KeyboardButton(opts[3])
                markup.row(itembtnone, itembtntwo)
                markup.row(itembtnthree, itembtnfour)
                bot.send_message(message.chat.id, u'Choose one option:', reply_markup=markup)
                cont = cont+1

            else:
                #Storing the last one
                answers.insert(cont - 1, message.text)
                answering = False
                bot.send_message(message.chat.id, u'Checking your answers...')
                bot.send_message(message.chat.id, "Your answers are: "+answers[0]+", "+answers[1]+", "+answers[2])
                # Connecting to the database to check
                markup = types.ReplyKeyboardRemove(selective=False)
                # if (message.text == u'Madrid'):
                #     bot.reply_to(message, u'Congratulations, you are right!', reply_markup=markup)
                # else:
                #     bot.reply_to(message, u'You are wrong!', reply_markup=markup)

                bot.send_message(message.chat.id,"You have answered the 90% of the answers correctly", reply_markup=markup)
                requested = False

    else:
        bot.reply_to(message, u'Request more questions to answer!')


bot.polling()
