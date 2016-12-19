import os
from queue import Queue

from droids import Sbb8
from slack_comm import SlackComm

IN_QUEUE = Queue()
OUT_QUEUE = Queue()

BOT_ID = os.environ.get("BOT_ID")
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
COMMAND_REGEX = r'\.do .*'


def start():
    sbb8 = Sbb8(BOT_ID, IN_QUEUE, OUT_QUEUE)
    sbb8.start()
    slack_comm = SlackComm(BOT_ID, IN_QUEUE, OUT_QUEUE, SLACK_BOT_TOKEN, COMMAND_REGEX)
    slack_comm.start()

    while True:
        pass

if __name__ == '__main__':
    start()
