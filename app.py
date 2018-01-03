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
        'store',
        'borrow',
        'stock',
        'lie',
        'num',
        'die1',
        'die21',
        'die22',
        'die31',
        'die32',
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'store',
            'conditions': 'is_going_to_store'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'borrow',
            'conditions': 'is_going_to_borrow'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'stock',
            'conditions': 'is_going_to_stock'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'lie',
            'conditions': 'is_going_to_lie'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'num',
            'conditions': 'is_going_to_num'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'die1',
            'conditions': 'is_going_to_die1'
        },
        {
            'trigger': 'advance',
            'source': 'die1',
            'dest': 'die21',
            'conditions': 'is_going_to_die21'
        },
        {
            'trigger': 'advance',
            'source': 'die1',
            'dest': 'die22',
            'conditions': 'is_going_to_die22'
        },
        {
            'trigger': 'advance',
            'source': 'die21',
            'dest': 'die31',
            'conditions': 'is_going_to_die31'
        },
        {
            'trigger': 'advance',
            'source': 'die21',
            'dest': 'die32',
            'conditions': 'is_going_to_die32'
        },
        {
            'trigger': 'go_back',
            'source': [
                'store',
                'borrow',
                'stock',
                'lie',
                'num',
                'die22',
                'die31',
                'die32'
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
