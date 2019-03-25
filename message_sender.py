import atexit
import logging

from telegram.ext import CommandHandler, MessageHandler, Filters

from helpers import UserHandler, BotHandler


def message_callback(bot, update):
    logging.info("Bot is being distracted by " + str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text="Please don't talk to me, I have to concentrate. Lives could be endangered!")


class Sender:
    def __init__(self, token):
        self.user_handler = UserHandler()
        self.bot_handler = BotHandler(token)
        self.updater = self.bot_handler.updater
        self.dispatcher = self.bot_handler.dispatcher
        logging.info("Sender initialised.")
        atexit.register(self.at_exit)

    def at_exit(self):
        logging.info("Exiting")
        self.updater.stop()

    def start_callback(self, bot, update):
        chat_id = update.message.chat_id
        if not self.user_handler.has_user(chat_id):
            logging.info("New chat started with " + str(update.message.chat_id))
            bot.send_message(chat_id=chat_id, text="Welcome I am your test bot.")
            self.user_handler.add_user(chat_id)
        else:
            logging.info("Chat started again with " + str(update.message.chat_id))
            bot.send_message(chat_id=chat_id, text="We already know each other, but still welcome back.")

    def remove_callback(self, bot, update):
        logging.info("Removing user callback")
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text="I am really sad that you want to leave, but I have to accept your wishes.")
        self.user_handler.remove_user(chat_id)

    def setup_handlers(self):
        command_handler = CommandHandler("start", self.start_callback)
        remove_handler = CommandHandler("remove", self.remove_callback)
        message_handler = MessageHandler(filters=Filters.text, callback=message_callback)
        self.dispatcher.add_handler(command_handler)
        self.dispatcher.add_handler(remove_handler)
        self.dispatcher.add_handler(message_handler)
        self.updater.start_polling(poll_interval=5)
        logging.info("Setting up handler. Starting to poll events now.")

    def send_message_to_all_chats(self, message):
        self.user_handler.update_users()
        users = self.user_handler.users
        if users.__len__() == 0:
            logging.info("No users registered to notify.")
            return
        logging.info("Sending message to all " + str(users.__len__()) + " users: " + message)
        for user in users:
            self.bot_handler.bot.send_message(chat_id=user, text=message)
