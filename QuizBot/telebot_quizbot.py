# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 18:32:13 2017

@author: Javier
"""
import telebot
from telebot import types
from DB.DBInterface import *
import random
import numpy as np
import enchant

bot = telebot.TeleBot("335396227:AAEJ5MWykURPRRFTMNso2NFT90o6Jn93bz8")
state_requested = None
state_answering = None
state_theme = None
state_asking = None
difficulty = ''
theme = ''
answers = []
questions = []
answers_user=[]
answers_factor=[]

percentage_options=0.6
cut_index=0

cont = 0
correct = 0
correct_answer = ''
index_themes = 0

spell_checker = enchant.Dict("en_US")
@bot.message_handler(commands=[u'start', u'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, u'Welcome to quizBot. Use /push to ask a question and /quiz to request questions from me')

@bot.message_handler(commands=[u'push'])
def push(message):
    global state_asking
    bot.send_message(message.chat.id, u'Ask me whatever you want and I will try to answer it!')
    state_asking=True

@bot.message_handler(commands=[u'quiz'])
def pull(message):
    global state_requested
    global state_answering
    global cont
    global state_theme
    global index_themes
    global answers_user
    global answers_factor
    global spell_checker


    cont=0
    answers_user=[]
    answers_factor=[]


    index_themes=0
    bot.send_message(message.chat.id, u'You have requested to get quiz answers')
    # Connecting to the database
    # Get difficulties from connector
    difficulties = DBInterace.GetDifficulty()
    #print difficulties[1].difficulty
    # We have to predefine the number of difficulties
    markup = types.ReplyKeyboardMarkup()
    itembtnone = types.KeyboardButton(difficulties[0].difficulty)
    itembtntwo = types.KeyboardButton(difficulties[1].difficulty)
    itembtnthree = types.KeyboardButton(difficulties[2].difficulty)
    markup.row(itembtnone, itembtntwo)
    markup.row(itembtnthree)
    bot.send_message(message.chat.id, u'Choose a difficulty:', reply_markup=markup)
    state_theme = True


@bot.message_handler(func=lambda message: True)
def check_answer(message):
    global state_requested
    global state_answering
    global state_theme
    global next

    global difficulty
    global theme
    global questions
    global answers

    global cont
    global correct

    global correct_answer

    global answers_factor
    global answers_user

    global index_themes

    global percentage_options

    global cut_index

    if(message.text==u'-NEXT-'):
        #Set states to enter again into the theme selection
        state_requested = False


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
            dif = DBInterace.GetDifficultyByLabel(difficulty);
            th = DBInterace.GetThemeByLabelAndParent(theme, 0);
            questions = DBInterace.GetUnknownQuestions(difficulty=dif, theme=th.id);

            if (len(questions)>10):
                questions=questions[0:10]

            print(len(questions))

            #Caulculate the cut_index
            cut_index=round(percentage_options*len(questions))

            print(cut_index)

            # Send the first question

            if questions:
                q = questions[cont].text

                # Query to the connector to get the options to that question
                answer = DBInterace.GetAnswer(question=questions[cont].id)

                opts = DBInterace.GetQuizAnswers(question=questions[cont])
                answers=[opts[0][0].text,opts[1][0].text,opts[2][0].text,opts[3][0].text]
                random.shuffle(answers)


                #sort the answers by frequency
                #choose the first, that one is the correct
                #get randomly other 3
                #update opts to send them to the user
                correct_answer= opts[0][0].text

                bot.send_message(message.chat.id, u'Question ' + str(cont + 1))
                bot.send_message(message.chat.id, q)
                markup = types.ReplyKeyboardMarkup()

                itembtnone = types.KeyboardButton(answers[0])
                itembtntwo = types.KeyboardButton(answers[1])
                itembtnthree = types.KeyboardButton(answers[2])
                itembtnfour = types.KeyboardButton(answers[3])
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
            suggestions = spell_checker.suggest(message.text)
            q = questions[cont].text
            if cont < questions.__len__() - 1:

                if correct_answer == message.text or (len(suggestions) != 0 and suggestions[0] == correct_answer):
                    bot.send_message(message.chat.id, u'Correct!')
                    correct = correct + 1
                    answers_user.append(1)

                else:
                    bot.send_message(message.chat.id, u'Incorrect!')
                    answers_user.append(0)

                answers_factor.append(0.5) if cont < cut_index else answers_factor.append(1.5)
                cont = cont + 1
                # print cont
                # next question
                q = questions[cont].text

                # Query to the connector to get the options to that question
                opts = DBInterace.GetQuizAnswers(question=questions[cont])
                # sort the answers by frequency
                # choose the first, that one is the correct
                # get randomly other 3
                # update opts to send them to the user
                # correct_answer=   - save here the correct one
                answers=[opts[0][0].text,opts[1][0].text,opts[2][0].text,opts[3][0].text]
                random.shuffle(answers)


                correct_answer = opts[0][0].text

                bot.send_message(message.chat.id, u'Question ' + str(cont + 1))
                bot.send_message(message.chat.id, q)

                if(cont<cut_index):
                    markup = types.ReplyKeyboardMarkup()
                    itembtnone = types.KeyboardButton(answers[0])
                    itembtntwo = types.KeyboardButton(answers[1])
                    itembtnthree = types.KeyboardButton(answers[2])
                    itembtnfour = types.KeyboardButton(answers[3])
                    markup.row(itembtnone, itembtntwo)
                    markup.row(itembtnthree, itembtnfour)
                    bot.send_message(message.chat.id, u'Choose one option:', reply_markup=markup)
                else:
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(message.chat.id, u'Type the answer', reply_markup=markup)



            else:
                if correct_answer == message.text or (len(suggestions) != 0 and suggestions[0] == correct_answer):
                    bot.send_message(message.chat.id, u'Correct!')
                    correct = correct + 1
                    answers_user.append(1)
                else:
                    bot.send_message(message.chat.id, u'Incorrect!')
                    answers_user.append(0)

                answers_factor.append(0.5) if cont < cut_index else answers_factor.append(1.5)
                cont = cont + 1
                # print cont
                # print correct


                state_answering = False

                markup = types.ReplyKeyboardRemove(selective=False)

                a = np.array(answers_user)
                b = np.array(answers_factor)

                score = sum(a * b) / sum(answers_factor)

                #percentage = (float(correct) / float(cont)) * 100

                bot.send_message(message.chat.id,
                                 u'Your score is ' + str(round(score,2)) + u' out of 1',
                                 reply_markup=markup)

                #here once you have estimated the user knowledge, save it to the db?
                #send to the user a course link according to the knowledge
                print (theme)
                print (difficulty)
                t=DBInterace.GetThemeByLabelAndParent(label=theme,parent=0)
                d=DBInterace.GetDifficultyByLabel(difficulty)

                course_dif = -1
                print "Score", score, "ID", d.id
                m = u"We have nothing to help you, you are too stupid or too smart"
                hard_difficulty_id = DBInterace.GetDifficultyByLabel("Hard").id
                easy_difficulty_id = DBInterace.GetDifficultyByLabel("Easy").id

                if(score<=0.25):
                    if(d.id != easy_difficulty_id):
                        course_dif = d.id - 1
                        m = u"You should try an easier quiz. We recommend you this course to improve:"
                    else:
                        course_dif = d.id
                        m = u"You are too stupid, but try this, try not to cry."

                elif(score>0.25 and score<0.75):
                        course_dif=d.id
                        m=u'We recommend you this course:'
                else:
                    if(d.id != hard_difficulty_id):
                        course_dif=d.id+1
                        m = u"You should try a harder quiz. We recommend you this course to improve:"
                    else:
                        course_dif = d.id
                        m = u"Ok, you are too good, this is the best offer for you, or go to arxiv.org"

                if course_dif < 0:
                    source = "No link"
                else:
                    source = DBInterace.GetSource(difficulty=course_dif, theme=t)[0].website

                #print(source[0].website)


                bot.send_message(message.chat.id,m,reply_markup=markup)
                bot.send_message(message.chat.id, source, reply_markup=markup)

                state_requested = False
                state_theme = False

    else:

        if state_theme:
            if(message.text != u'-NEXT-'):
                difficulty = message.text
            # Getting themes from connector
            themes = DBInterace.GetTheme()

            # We have to predefine the number of themes by default
            buttons = [item.label for item in themes]

            final_button = u'-NEXT-' if len(buttons)-1 > index_themes + 5 else u'-END-'
            print final_button
            markup = types.ReplyKeyboardMarkup()
            itembtnone = types.KeyboardButton(buttons[index_themes+1])
            itembtntwo = types.KeyboardButton(buttons[index_themes+2])
            itembtnthree = types.KeyboardButton(buttons[index_themes+3])
            itembtnfour = types.KeyboardButton(buttons[index_themes+4])
            itembtnfive = types.KeyboardButton(buttons[index_themes+5])
            itembtnsix = types.KeyboardButton(final_button)
            markup.row(itembtnone, itembtntwo, itembtnthree)
            markup.row(itembtnfour, itembtnfive, itembtnsix)

            index_themes=index_themes+5 if len(buttons)>index_themes+10 else len(buttons)-6


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
