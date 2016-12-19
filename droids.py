import re
import threading

import time

import logging

from commands import COMMANDS
from message import Message

READ_WEB_SOCKET_DELAY = 1


class Sbb8(threading.Thread):
    def __init__(self, bot_id, in_queue, out_queue, group=None, target=None, name=None, args=(), kwargs=None, *,
                 daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._bot_id = bot_id
        self._in_queue = in_queue
        self._out_queue = out_queue

    def run(self):
        while True:
            if not self._in_queue.empty():
                message = self._in_queue.get()
                response_message = self._process_message(message)
                self._out_queue.put(response_message)

            time.sleep(READ_WEB_SOCKET_DELAY)

    def _process_message(self, message: Message):
        response_message = Message()
        response_message.channel = message.channel

        if message.kind == Message.Kind.TEXT:
            response_message.payload = 'No comprende'
        else:
            response_message.payload = self._process_command(message)

        return response_message

    @staticmethod
    def _process_command(message):
        logging.debug('Processing command [%s]' % message.payload)
        for c in COMMANDS:
            if c['regex'].match(message.payload):
                return c['command']()

        logging.error('Command not executed %s' % message.payload)
        return "Do not understand the command"
