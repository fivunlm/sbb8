import re
import threading

import logging

import time
from slackclient import SlackClient

from message import Message

READ_WEB_SOCKET_DELAY = 1


class SlackComm(threading.Thread):
    def __init__(self, bot_id, in_queue, out_queue, slack_bot_token, command_regex, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._bot_id = bot_id
        self._in_queue = in_queue
        self._out_queue = out_queue
        self._slack_bot_token = slack_bot_token
        self._slack_client = SlackClient(slack_bot_token)
        self._command_regex = re.compile(command_regex)

    def run(self):

        if not self._slack_client.rtm_connect():
            logging.error("Connection failed. Invalid Slack token or bot ID?")
            return

        logging.debug("StarterBot connected and running!")
        while True:

            # Check if we have some input from slack
            message = self._parse_slack_output(self._slack_client.rtm_read())
            if message is not None:
                self._in_queue.put(message)

            if not self._out_queue.empty():
                self._send_message(self._out_queue.get())

            time.sleep(READ_WEB_SOCKET_DELAY)

    def _parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        input_list = slack_rtm_output

        if input_list and len(input_list) > 0:
            for input_entry in input_list:
                logging.debug(input_entry)
                if input_entry and 'text' in input_entry and self._bot_id != input_entry['user']:
                    message = Message(
                        Message.Kind.COMMAND if self._command_regex.match(input_entry['text']) else Message.Kind.TEXT,
                        input_entry['text'], input_entry['channel'])
                    return message

        # logging.warning('Unknown slack message: %s' % input_list)
        return None

    def _send_message(self, message: Message):
        if message.kind != Message.Kind.TEXT:
            logging.error('Out message is not TEXT')
            return
        self._slack_client.api_call("chat.postMessage", channel=message.channel,
                                    text=message.payload, as_user=True)
