import csv
from datetime import datetime
from opengs_maptool.models.console import Console
from opengs_maptool.models.message import Message, MessageAuthor, MessageType

class ConsoleService:
    def load(self, path: str) -> Console:
        """
        Load a CSV file from disk containing a message history

        @param path: The file path
        """
        console = Console()

        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            data = [row for row in reader]

            # Check that the header structure of the CSV file is correct
            csv_header = data[0]
            if (
                csv_header[0] != "text"
                or csv_header[1] != "author"
                or csv_header[2] != "datetime"
                or csv_header[3] != "type"
            ):
                raise Exception("The structure of the CSV header for the console history is incorrect")

            # Retrieves the messages and adds them to the console
            for message_data in data[1:]:
                message = Message(
                    str(message_data[0]),
                    MessageAuthor(message_data[1]),
                    datetime.fromisoformat(message_data[2]),
                    MessageType(message_data[3])
                )
                console.add_message(message)

        return console


    def save(self, console: Console, path: str):
        """
        Saves the message history of a console to disk in CSV format
                
        @param console: The console containing the message history
        @param path: The file path
        """
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["text", "author", "datetime", "type"])
            
            for message in console.messages:
                writer.writerow([
                    message.text,
                    message.author.value,
                    message.datetime,
                    message.type.value
                ])


    def add_message(self, console: Console, message: Message):
        """
        Add a message to a console (model)

        @param console: The console
        @param message: The message to add
        """
        console.add_message(message)


    def get_user_command_history(self, console: Console) -> list[Message]:
        """
        Retrieves all messages sent by the user from a console

        @param console: The console
        """
        history = []
        for message in console.messages:
            if message.author == MessageAuthor.USER:
                history.append(message)
        
        return history


    def clear_console(self, console: Console):
        """
        Delete all messages
        """
        console.clear()
