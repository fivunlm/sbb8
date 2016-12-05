import threading


class Sbb8(threading.Thread):
    def __init__(self, bot_id, in_queue, out_queue, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._bot_id = bot_id
        self._in_queue = in_queue
        self._out_queue = out_queue

    def run(self):
        pass

