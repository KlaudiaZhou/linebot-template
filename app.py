import os
import sys

from argparse import ArgumentParser
from datetime import datetime
from glob import glob
from time import sleep

from flask import Flask, request, abort, Response, send_from_directory
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
    TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
)

app = Flask(__name__)
channel_secret = "9b74e5a2e19a7ef8b93f1ae7415cc699"
channel_access_token = "oJ5JiZ3p6ixcVGp5aMH50McVRFcuin6CFcDqopJ68nJrX0N+qKu1at/BHM1mUeQm7DO8On7jT9hT2ga/X+Cvo8cw4INeS+cEjsOThXD8pVjIUlFjLzLlS0lPUHnkHDkbJZuc3b1oTikIvVJWjXUqQAdB04t89/1O/w1cDnyilFU="

if channel_secret is None:
    print("Please specify LINE_CHANNEL_SECRET.")
    sys.exit(1)
if channel_access_token is None:
    print("Please specify LINE_CHANNEL_ACCESS_TOKEN.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    if event.source.user_id == "Udeadbeefdeadbeefdeadbeefdeadbeef":
        return
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=echo(event))
    )


def echo(event):
    return event.message.text


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python3 " + __file__ + " [--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", default=8000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")
    arg_parser.add_argument("-n", "--ngrok", required=True, help="ngrok")
    options = arg_parser.parse_args()

    # Run
    app.config["ngrok"] = options.ngrok 
    app.run(debug=options.debug, port=options.port)