# app/widgets/dm_chat_widget.py

"""This module displays a history of user submitted text and AI generated text."""

from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout

class DMChatWidget(QWidget):
    """Widget to display Dungeon Master's messages and conversation history."""

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Game:")
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.chat_box)

    def append_user_message(self, message: str):
        """Append a user message to the chat box."""
        self.chat_box.append(f"<b>You:</b> {message}")

    def append_dm_message(self, message: str):
        """Append a Dungeon Master message to the chat box."""
        self.chat_box.append(f"<b>DM:</b> {message}")

    def clear_chat(self):
        """Clear the chat history."""
        self.chat_box.clear()
