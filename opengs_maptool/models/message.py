from enum import Enum

class Message:
    class MessageAuthor(Enum):
        SYSTEM = "system"
        USER = "user"
    
    class MessageType(Enum):
        NORMAL = 0
        INFO = 1
        SUCCESS = 2
        WARNING = 3
        ERROR = 4

    def __init__(self, text: str, author: MessageAuthor, datetime, type: MessageType = MessageType.NORMAL):
        self.text = text
        self.author = author
        self.datetime = datetime
        self.type = type
