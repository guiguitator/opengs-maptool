from opengs_maptool.models.message import Message

class Console:
    def __init__(self):
        self.message_history: list[Message] = []

    def add_message(self, message: Message):
        self.message_history.append(message)
