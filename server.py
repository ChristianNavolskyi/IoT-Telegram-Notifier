import logging
import os

from bottle import run, route, default_app

from message_sender import Sender


@route("/")
def welcome():
    return "Welcome on our notification platform. This is where lives are saved."


@route("/emergency/<message>/")
@route("/emergency/<message>")
@route("/emergency/")
@route("/emergency")
def test(message=None):
    logging.info("Emergency was triggered.")
    emergency_text = "There is an emergency!"
    if message:
        emergency_text = str(message)
    sender.send_message_to_all_chats(emergency_text)
    return emergency_text


if __name__ == '__main__':
    token = os.environ["TOKEN"]
    sender = Sender(token)

    app = default_app()
    run(host="0.0.0.0", port=80, debug=True)
