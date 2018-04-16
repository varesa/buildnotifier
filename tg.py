import os
from telegram.ext import Updater, CommandHandler


class Tg:
    def __init__(self, logger):
        self.logger = logger

        self.full = []
        self.builds = []

        # Initialize the telegram API
        self.updater = Updater(token=os.environ['TELEGRAM_TOKEN'])
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot

        # Register the command handlers
        start_handler = CommandHandler('start', self.start)
        full_handler = CommandHandler('full', self.register_full)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(full_handler)

        logger.info("Starting telegram polling")
        self.updater.start_polling()

    def start(self, bot, update):
        """
        Handler for the /start command. Send instructions
        """
        self.logger.info("Received /start. Chat ID:" + str(update.message.chat_id))
        self.logger.info("Sending instructions")

        bot.send_message(chat_id=update.message.chat_id, text="Hello. Type /builds to receive build status notifications or /full to get full build information")

    # Telegram command handlers

    def register_full(self, bot, update):
        self.logger.info("Received /full. Chat ID: " + str(update.message.chat_id))
        self.full.append(update.message.chat_id)
        bot.send_message(chat_id=update.message.chat_id, text="You will now receive full build information. Type /off to disable")

    def register_builds(self, bot, update):
        self.logger.info("Received /builds. Chat ID: " + str(update.message.chat_id))
        self.builds.append(update.message.chat_id)
        bot.send_message(chat_id=update.message.chat_id, text="You will now receive short build information. Type /off to disable")

    # Wrappers to send specific messages

    def send_build(self, build):
        for chat_id in self.full:
            self.bot.send_message(chat_id=chat_id, text="Building " + build)

    def send_stage(self, stage):
        for chat_id in self.full:
            self.bot.send_message(chat_id=chat_id, text="Build entered stage " + stage)

    def send_complete(self, url):
        for chat_id in set(self.full):
            self.bot.send_message(chat_id=chat_id, text="Build complete: " + url)