class Message:
    class Kind:
        TEXT = 100
        COMMAND = 200

    def __init__(self, kind=Kind.TEXT, payload=None, channel=None):
        self.kind = kind
        self.payload = payload
        self.channel = channel
