import logging
import os

from telegram import Bot
from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class BotHandler:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.updater = Updater(bot=self.bot)
        self.dispatcher = self.updater.dispatcher

    def stop_polling(self):
        logging.info("Exiting")
        self.updater.stop()

    def add_handlers(self, *handlers):
        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def start_polling(self, poll_interval=None):
        self.updater.start_polling(poll_interval=poll_interval)


class UserHandler:
    def __init__(self):
        self.user_file_name = ".users"
        self.update_users()

    def update_users(self):
        try:
            user_file = open(self.user_file_name, "r")
        except FileNotFoundError:
            open(self.user_file_name, "w+").close()
            self.users = []
            return
        self.users = user_file.read().splitlines()
        user_file.close()

    def has_user(self, user_id):
        self.update_users()
        return any(str(user_id) in user for user in self.users)

    def add_user(self, user_id):
        logging.info("Adding user: " + str(user_id))
        if self.has_user(user_id):
            return
        user_file = open(self.user_file_name, "a")
        user_file.write(str(user_id) + "\n")
        user_file.close()

    def remove_user(self, user_id):
        user_id_str = str(user_id)
        logging.info("Removing user " + user_id_str)
        try:
            self.users.remove(user_id_str)
        except ValueError:
            return
        os.remove(self.user_file_name)
        user_file = open(self.user_file_name, "w+")
        for user in self.users:
            user_file.write(str(user) + "\n")
        user_file.close()
