import logging
import os

from bottle import run, route, default_app, post, request

from message_sender import Sender


@route("/")
def welcome():
    return "Welcome on our notification platform. This is where lives are saved."


@post("/emergency")
@post("/emergency/")
def post_emergency():
    logging.info("Emergency was triggered.")
    emergency_text = "There is an emergency!"

    forms = request.forms

    post_message = forms.get("message")
    post_lon = forms.get("lon")
    post_lat = forms.get("lat")

    if post_message:
        emergency_text = str(post_message)

    sender.send_message_to_all_chats(emergency_text, lon=post_lon, lat=post_lat)


if __name__ == '__main__':
    token = os.environ["TOKEN"]
    sender = Sender(token)

    app = default_app()
    run(host="0.0.0.0", port=80, debug=True)
