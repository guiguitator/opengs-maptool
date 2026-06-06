from enum import Enum

class MessageType(Enum):
    NORMAL = "normal"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

class MessageAuthor(Enum):
    SYSTEM = "system"
    USER = "user"

class Message:
    def __init__(self, text: str, author: MessageAuthor, datetime, type: MessageType = MessageType.NORMAL):
        self.text = text
        self.author = author
        self.datetime = datetime
        self.type = type
