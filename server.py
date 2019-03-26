import logging
import os

from bottle import run, route, default_app

from message_sender import Sender


@route("/emergency/<location>/")
@route("/emergency/<location>")
@route("/emergency/")
@route("/emergency")
def test(location=None):
    logging.info("Emergency was triggered.")
    emergency_text = "There is an emergency!"
    if location:
        emergency_text = "There is an emergency at " + str(location) + "!"
    sender.send_message_to_all_chats(emergency_text)


if __name__ == '__main__':
    token = os.environ["TOKEN"]
    sender = Sender(token)

    app = default_app()
    run(host="0.0.0.0", port=80, debug=True)
