import json
import os
import requests
from telegram.ext import Updater, CommandHandler


class Tg:
    def __init__(self, logger):
        self.logger = logger

        self.full = []
        self.builds = []
        self.load_chats()

        # Initialize the telegram API
        self.updater = Updater(token=os.environ['TELEGRAM_TOKEN'])
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot

        # Register the command handlers
        start_handler = CommandHandler('start', self.start)
        builds_handler = CommandHandler('builds', self.register_builds)
        full_handler = CommandHandler('full', self.register_full)
        unregister_handler = CommandHandler('off', self.unregister)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(builds_handler)
        self.dispatcher.add_handler(full_handler)
        self.dispatcher.add_handler(unregister_handler)

        logger.info("Starting telegram polling")
        self.updater.start_polling()

    def start(self, bot, update):
        """
        Handler for the /start command. Send instructions
        """
        self.logger.info("Received /start. Chat ID:" + str(update.message.chat_id))
        self.logger.info("Sending instructions")

        bot.send_message(chat_id=update.message.chat_id, text="Hello. Type /builds to receive build status notifications or /full to get full build information")

    def save_chats(self):
        with open("/data/chats", 'w') as file:
            json.dump({'full': self.full, 'builds': self.builds}, file)
            self.logger.info("Saving chat_ids to file")

    def load_chats(self):
        try:
            with open("/data/chats", 'r') as file:
                data = json.load(file)
                self.full = data['full']
                self.builds = data['builds']
                self.logger.info("Loaded the following chat_ids from file: " + str(self.full) + ", " + str(self.builds))
        except FileNotFoundError:
            self.logger.info("Unable to load chat_ids, going with empty defaults")

    # Telegram command handlers

    def register_full(self, bot, update):
        self.logger.info("Received /full. Chat ID: " + str(update.message.chat_id))
        if update.message.chat_id not in self.full:
            self.logger.info("Adding ID to full")
            self.full.append(update.message.chat_id)
        if update.message.chat_id in self.builds:
            self.logger.info("Removing ID from builds")
            self.builds.remove(update.message.chat_id)
        self.save_chats()
        bot.send_message(chat_id=update.message.chat_id, text="You will now receive full build information. Type /off to disable")

    def register_builds(self, bot, update):
        self.logger.info("Received /builds. Chat ID: " + str(update.message.chat_id))
        if update.message.chat_id not in self.builds:
            self.logger.info("Adding ID to builds")
            self.builds.append(update.message.chat_id)
        if update.message.chat_id in self.full:
            self.logger.info("Removing ID from full")
            self.full.remove(update.message.chat_id)
        self.save_chats()
        bot.send_message(chat_id=update.message.chat_id, text="You will now receive short build information. Type /off to disable")

    def unregister(self, bot, update):
        self.logger.info("Received /off. Chat ID: " + str(update.message.chat_id))
        if update.message.chat_id in self.builds:
            self.logger.info("Removing ID from builds")
            self.builds.remove(update.message.chat_id)
        if update.message.chat_id in self.full:
            self.logger.info("Removing ID from full")
            self.full.remove(update.message.chat_id)
        self.save_chats()
        bot.send_message(chat_id=update.message.chat_id, text="You should no longer receive updates")

    # Wrappers to send specific messages

    def send_build(self, build):
        for chat_id in self.full:
            self.bot.send_message(chat_id=chat_id, text="Building " + build)

    def send_stage(self, stage):
        for chat_id in self.full:
            self.bot.send_message(chat_id=chat_id, text="Build entered stage " + stage)

    def send_complete(self, url):
        r = requests.get(url + "api/json")

        data = r.json()
        testAction = {}
        for action in data['actions']:
            if action.get('_class', '') == "hudson.tasks.junit.TestResultAction":
                testAction = action

        msg = "Build #" + str(data['id']) + " " + data['result'] + " (" + url + ")."
        if testAction.get('failCount', 0) != 0:
            msg += " Tests failed: " + str(testAction['failCount'])

        for chat_id in set(self.full + self.builds):
            self.bot.send_message(chat_id=chat_id, text=msg)
