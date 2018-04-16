from flask import Flask, redirect, render_template, request
import logging
from telegram.ext import Updater, CommandHandler
from time import sleep

logger = logging.getLogger("buildnotifier")
logger.setLevel(LOG_LEVEL)
handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Telegram

def start(bot, update):
    """
    Handler for the /start command. Send instructions
    """
    logger.info("Received /start. Chat ID:" + str(update.message.chat_id))
    logger.info("Sending instructions")

    bot.send_message(chat_id=update.message.chat_id, text="Hello. Type /builds to receive build status notifications or /full to get full build information")

full = []

def full(bot, update):
	logger.info("Received /full. Chat ID: " + str(update.message.chat_id))
	full.append(update.message.chat_id)
	bot.send_message(chat_id=update.message.chat_id, text="You will now receive full build information. Type /off to disable")

logger.info("Starting")

token = os.environ['TELEGRAM_TOKEN']

# Initialize the telegram API
updater = Updater(token=token)
dispatcher = updater.dispatcher

# Register the command handlers
start_handler = CommandHandler('start', start)
full_handler = CommandHandler('full', full)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(full_handler)

logger.info("Starting telegram polling")
updater.start_polling()

# Flask

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post():
    data = request.json
    if data['type'] == 'stage':
        print('Running stage: ' + data['stage'])

    if data['type'] == 'complete':
        print('Build complete: ' + data['url'])
    return ''

@app.route('/health')
def healthcheck():
    return 'OK'

