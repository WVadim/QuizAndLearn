# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 18:32:13 2017

@author: Javier
"""
import telebot
from telebot import types
from DBInterface import *

bot = telebot.TeleBot("335396227:AAEJ5MWykURPRRFTMNso2NFT90o6Jn93bz8")
state_requested = None
state_answering = None
state_theme = None
state_asking = None
difficulty = ''
theme = ''
answers = []
questions = []
cont = 0
correct = 0
correct_answer = ''


@bot.message_handler(commands=[u'start', u'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, u'I\'m a bot, please talk to me!')
    #meter aqui instrucciones del bot

@bot.message_handler(commands=[u'push'])
def push(message):
    global state_asking
    bot.send_message(message.chat.id, u'Ask me whatever you want and I will try to answer it!')
    state_asking=True

@bot.message_handler(commands=[u'pull'])
def pull(message):
    global state_requested
    global cont
    global state_theme
    bot.send_message(message.chat.id, u'You have requested to get quiz answers')
    # Connecting to the database
    # Get difficulties from connector
    difficulties = DBInterace.GetDifficulty()
    # We have to predefine the number of difficulties
    markup = types.ReplyKeyboardMarkup()
    itembtnone = types.KeyboardButton(difficulties[0])
    itembtntwo = types.KeyboardButton(difficulties[1])
    itembtnthree = types.KeyboardButton(difficulties[2])
    markup.row(itembtnone, itembtntwo)
    markup.row(itembtnthree)
    bot.send_message(message.chat.id, u'Choose a difficulty:', reply_markup=markup)
    state_theme = True


@bot.message_handler(func=lambda message: True)
def check_answer(message):
    global state_requested
    global state_answering
    global state_theme

    global difficulty
    global theme
    global questions
    global answers

    global cont
    global correct

    global correct_answer

    if (state_requested):
        if (state_answering != True):
            cont = 0
            correct = 0
            theme = message.text
            # Get random questions of Geography from the connector according to the theme
            # print(theme)
            # print(difficulty)
            #here we have to place the method to get questions of a certain theme and difficulty
            #questions = getQuestions(theme, difficulty)
            # Send the first question

            if questions:
                q = questions[cont]

                # Query to the connector to get the options to that question
                opts = DBInterace.getAnswer(question=q)
                #sort the answers by frequency
                #choose the first, that one is the correct
                #get randomly other 3
                #update opts to send them to the user
                #correct_answer=   - save here the correct one

                bot.send_message(message.chat.id, u'Question ' + str(cont + 1))
                bot.send_message(message.chat.id, q)
                markup = types.ReplyKeyboardMarkup()
                itembtnone = types.KeyboardButton(opts[0])
                itembtntwo = types.KeyboardButton(opts[1])
                itembtnthree = types.KeyboardButton(opts[2])
                itembtnfour = types.KeyboardButton(opts[3])
                markup.row(itembtnone, itembtntwo)
                markup.row(itembtnthree, itembtnfour)
                bot.send_message(message.chat.id, u'Choose one option:', reply_markup=markup)
                state_answering = True

            else:
                state_theme = False
                state_requested = False
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(message.chat.id,
                                 u'Uh-oh, currently there are no questions available for that theme and difficulty.',
                                 reply_markup=markup)



        else:
            q = questions[cont]
            if cont < questions.__len__() - 1:
                if correct_answer == message.text:
                    bot.send_message(message.chat.id, u'Correct!')
                    correct = correct + 1
                else:
                    bot.send_message(message.chat.id, u'Incorrect!')

                cont = cont + 1
                # print cont
                # next question
                q = questions[cont]

                # Query to the connector to get the options to that question
                opts = DBInterace.getAnswer(question=q)
                # sort the answers by frequency
                # choose the first, that one is the correct
                # get randomly other 3
                # update opts to send them to the user
                # correct_answer=   - save here the correct one

                bot.send_message(message.chat.id, u'Question ' + str(cont + 1))
                bot.send_message(message.chat.id, q)
                markup = types.ReplyKeyboardMarkup()
                itembtnone = types.KeyboardButton(opts[0])
                itembtntwo = types.KeyboardButton(opts[1])
                itembtnthree = types.KeyboardButton(opts[2])
                itembtnfour = types.KeyboardButton(opts[3])
                markup.row(itembtnone, itembtntwo)
                markup.row(itembtnthree, itembtnfour)
                bot.send_message(message.chat.id, u'Choose one option:', reply_markup=markup)


            else:
                if correct_answer == message.text:
                    bot.send_message(message.chat.id, u'Correct!')
                    correct = correct + 1
                else:
                    bot.send_message(message.chat.id, u'Incorrect!')

                cont = cont + 1
                # print cont
                # print correct
                state_answering = False

                markup = types.ReplyKeyboardRemove(selective=False)

                percentage = (float(correct) / float(cont)) * 100

                bot.send_message(message.chat.id,
                                 u'You have answered the ' + str(percentage) + u'% of the answers correctly',
                                 reply_markup=markup)

                #here once you have estimated the user knowledge, save it to the db?
                #send to the user a course link according to the knowledge

                state_requested = False
                state_theme = False

    else:
        if state_theme:
            difficulty = message.text
            # Getting themes from connector
            themes = DBInterace.GetTheme()
            # We have to predefine the number of themes by default

            markup = types.ReplyKeyboardMarkup()
            itembtnone = types.KeyboardButton(themes[0])
            itembtntwo = types.KeyboardButton(themes[1])
            itembtnthree = types.KeyboardButton(themes[2])
            itembtnfour = types.KeyboardButton(themes[3])
            itembtnfive = types.KeyboardButton(themes[4])
            itembtnsix = types.KeyboardButton(themes[5])
            markup.row(itembtnone, itembtntwo, itembtnthree)
            markup.row(itembtnfour, itembtnfive, itembtnsix)
            bot.send_message(message.chat.id, u'Choose a theme:', reply_markup=markup)
            state_requested = True
            cont = 0


        else:
            if state_asking:
                # do here the get matching question thing
                # give the correct answer to the user
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.reply_to(message, u'I am giving you an answer', reply_markup=markup)
            else:
                markup = types.ReplyKeyboardRemove(selective=False)
                state_theme = False
                bot.reply_to(message, u'Request more questions to answer!', reply_markup=markup)


bot.polling()
