from datetime import datetime
from opengs_maptool.models.message import Message, MessageType, MessageAuthor

class CommandResponse:
    """Represents the result of executing a command, including a message and its type, and other return data."""

    def __init__(self, message: str, message_type: MessageType, return_data: dict | None = None):
        self.message = message
        self.message_type = message_type
        # self.return_data = return_data or {} # Any other return data

    def as_message(self) -> Message:
        """Returns the response as a Message object."""
        return Message(
            text=self.message,
            author=MessageAuthor.SYSTEM,
            datetime=datetime.now(),
            type=self.message_type
        )
