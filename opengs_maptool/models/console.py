from opengs_maptool.models.message import Message

class Console:
    def __init__(self):
        self.messages: list[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def clear(self):
        self.messages = []
