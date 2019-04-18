import atexit
import logging

from telegram import Location
from telegram.error import Unauthorized
from telegram.ext import CommandHandler, MessageHandler, Filters

from helpers import UserHandler, BotHandler


def message_callback(bot, update):
    logging.info("Bot is being distracted by " + str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text="Please don't talk to me, I have to concentrate. Lives could be endangered!")


class Sender:
    def __init__(self, token):
        self.user_handler = UserHandler()
        self.bot_handler = BotHandler(token)
        logging.info("Sender initialised.")
        atexit.register(self.bot_handler.stop_polling)
        self.setup_handlers()

    def start_callback(self, bot, update):
        chat_id = update.message.chat_id
        if not self.user_handler.has_user(chat_id):
            logging.info("New chat started with " + str(update.message.chat_id))
            bot.send_message(chat_id=chat_id, text="Thanks for your registration. You might be the one who will save a life!")
            self.user_handler.add_user(chat_id)
        else:
            logging.info("Chat started again with " + str(update.message.chat_id))
            bot.send_message(chat_id=chat_id, text="We already know each other, but still welcome back.")

    def remove_callback(self, bot, update):
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text="I am really sad that you want to leave, but I have to accept your wishes.")
        self.user_handler.remove_user(chat_id)

    def setup_handlers(self):
        command_handler = CommandHandler("start", self.start_callback)
        remove_handler = CommandHandler("remove", self.remove_callback)
        message_handler = MessageHandler(filters=Filters.text, callback=message_callback)
        self.bot_handler.add_handlers(command_handler, remove_handler, message_handler)
        self.bot_handler.start_polling(poll_interval=5)
        logging.info("Setting up handler. Starting to poll events now.")

    def send_message_to_all_chats(self, message, lon=None, lat=None):
        self.user_handler.update_users()
        users = self.user_handler.users

        if users.__len__() == 0:
            logging.info("No users registered to notify.")
            return

        location = None
        if lon and lat:
            location = Location(longitude=lon, latitude=lat)

        bot = self.bot_handler.bot
        logging.info("Sending message (\"{0}\") to all users ({1})".format(message, users))
        for i, user in enumerate(users):
            try:
                bot.send_message(chat_id=user, text=message)
                if location:
                    bot.send_location(chat_id=user, location=location)
            except Unauthorized:
                logging.info("User {0} blocked bot and will be removed".format(user))
                self.user_handler.remove_user(user_id=user)
