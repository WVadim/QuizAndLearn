from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
from telegram.ext import MessageHandler, Filters

#Updating the token
updater = Updater(token='335396227:AAEJ5MWykURPRRFTMNso2NFT90o6Jn93bz8')
dispatcher = updater.dispatcher
requested=None
#Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    
def pull(bot, update):
    global requested
    bot.sendMessage(chat_id=update.message.chat_id, text="You have requested to get quiz answers")
    #Connecting to the database
    bot.sendMessage(chat_id=update.message.chat_id, text="What is the capital city of Spain?")
    requested =True

def check_answer(bot, update):
    global requested
    if (requested):
        bot.sendMessage(chat_id=update.message.chat_id, text="Checking your answer")
        #Connecting to the database to check
        if(update.message.text=="Madrid"):  
            bot.sendMessage(chat_id=update.message.chat_id, text="Congratulations, you are right!")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="You are wrong!")
            
        requested=False
    
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Request more questions to answer!")

    
        
    
#Definition of the Command /start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

pull_handler = CommandHandler('pull', pull)
dispatcher.add_handler(pull_handler)

check_handler = MessageHandler(Filters.text, check_answer)
dispatcher.add_handler(check_handler)

#Runnnig the bot
updater.start_polling()
