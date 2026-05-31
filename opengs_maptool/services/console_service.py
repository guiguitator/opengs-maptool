from enum import Enum

from opengs_maptool.models.console import Console
from opengs_maptool.models.message import Message

class ConsoleService:
    def load(self, filename: str) -> Console:
        pass

    def save(self, console: Console, filename: str):
        pass

    def add_message(self, console: Console, message: Message):
        console.add_message(message)

    def get_history(self, console: Console) -> list[Message]:
        history = []
        for message in console.message_history:
            if message.author == Message.MessageAuthor.USER:
                history.append(message)
        
        return history
