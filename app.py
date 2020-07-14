import logging 
from flask import Flask,request
#request contains all the information about the current request 
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters , Dispatcher 
from telegram import Bot, Update,ReplyKeyboardMarkup
from utils import get_reply,fetch_news,topics_keyboard




#enable login 

# format of login 
# asctime - time at which the event happens 
# name - name of the function or class due to whiuch event happens
# levelname - login can have multiple level (information , warning , error)
# message - actual message 
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,
					level = logging.INFO)
logger = logging.getLogger(__name__)      #logger object - create logs for program
 
TOKEN = "1068406883:AAHxK7JXJ7GtabrfsLyrzwJ4WtO_qKe3J24"

# in order to create a flask application , first we need to create a flask object 
app = Flask(__name__)
#creating veiw - END POINT so that it can receive some request 
# route for Flask Application 

@app.route('/')
def index():
	return "Hello"

@app.route(f'/{TOKEN}',methods = ['Get','Post'])
def webhook():
	'''Webhook view which receives updates from telegram '''
	# create update object from json-format request data
	#telegram will be sending us updates in the form of json objects

	# from request() we get the json object and we convert it into telegram module
	update = Update.de_json(request.get_json(),bot)      # This line just creates an update object 
	#process update
	dp.process_update(update)				 # dp is the dispatcher object  which is responsible for handling the updates 
	return "ok"

def start(bot,update):
	print(update)
	author = update.message.from_user.first_name
	reply = "Hi ! {} ".format(author)
	bot.send_message(chat_id = update.message.chat_id,text=reply)

def _help(bot,update):
	help_text = "hey ! this is help text "
	bot.send_message(chat_id = update.message.chat_id,text=help_text)

def news(bot ,update):
	bot.send_message(chat_id=update.message.chat_id , text ="Choose a category",
		reply_markup=ReplyKeyboardMarkup(keyboard =topics_keyboard ,one_time_keyboard = True))

def reply_text(bot,update):
	intent,reply = get_reply(update.message.text,update.message.chat_id)
	if intent =="get_news":
		articles = fetch_news(reply)
		for article in articles :
			bot.send_message(chat_id = update.message.chat_id, text=article['link'])
	else :
		bot.send_message(chat_id = update.message.chat_id, text=reply)

def echo_sticker(bot,update):
	bot.send_sticker(chat_id = update.message.chat_id ,
					 sticker = update.message.sticker.file_id)

def error(bot,update):
	logger.error("Update '%s' caused errror '%s' ",update,update.error)

bot = Bot(TOKEN)
try:
	bot.set_webhook("https://elegant-choucroute-74500.herokuapp.com/" + TOKEN)	 		
except Exception as e:
	print(e)	
# need to have a perfectly working url so that anyone can access on the internet 
dp = Dispatcher(bot , None )
dp.add_handler(CommandHandler ("start" , start))
dp.add_handler(CommandHandler ("help" , _help))
dp.add_handler(CommandHandler ("news" , news))
dp.add_handler(MessageHandler (Filters.text , reply_text))
dp.add_handler(MessageHandler (Filters.sticker , echo_sticker))
dp.add_error_handler(error)
	

if __name__=="__main__":    #event 
	app.run(port = 8080)
	
