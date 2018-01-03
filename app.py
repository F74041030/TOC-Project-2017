import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine
import requests
from bs4 import BeautifulSoup

API_TOKEN = '546365152:AAEpWlT2pQ2KRKHfCvN1r80btyx88Cn9Fxk'
WEBHOOK_URL = 'https://a49feb28.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        '1',
        '2',
        '3',
        '4',
        '5'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': '1',
            'conditions': 'is_going_to_1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': '2',
            'conditions': 'is_going_to_2'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': '3',
            'conditions': 'is_going_to_3'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': '4',
            'conditions': 'is_going_to_4'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': '5',
            'conditions': 'is_going_to_5'
        },
        {
            'trigger': 'go_back',
            'source': [
                '1',
                '2',
                '3',
                '4',
                '5'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
