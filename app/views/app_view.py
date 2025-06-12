# app/views/app_view.py

"""This module defines the UI components that go into our main app page."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QTextEdit, QPushButton
)
from app.logic import AIHandler, LoadGame, ProcessGameInput

class AppView(QWidget):
    """
        Defines our main app view.
    """

    def __init__(self, name: str):
        super().__init__()
        self.ai_handler = AIHandler()
        self.world_data = LoadGame().get_world_data()
        self.process_input = ProcessGameInput(self.world_data)

        message = QLabel(f"Hello, {name}! Now choose your character info!" if name else "Hello!")
        message.setStyleSheet("font-size: 20px; color: green")

        layout = QVBoxLayout()
        layout.addWidget(message)

        #Character name input
        self.character_name_input = QLineEdit()
        self.character_name_input.setPlaceholderText("Enter your character name")
        layout.addWidget(QLabel("Character Name:"))
        layout.addWidget(self.character_name_input)

        #Character Race dropdown
        self.race_dropdown = QComboBox()
        self.race_dropdown.addItems(["Human" , "Dwarf" , "Elf"])
        layout.addWidget(QLabel("Race:"))
        layout.addWidget(self.race_dropdown)

        #Character Class dropdown
        self.class_dropdown = QComboBox()
        self.class_dropdown.addItems(["Fighter", "Mage", "Rogue"])
        layout.addWidget(QLabel("Class:"))
        layout.addWidget(self.class_dropdown)

        #Character Gender Dropdown
        self.gender_dropdown = QComboBox()
        self.gender_dropdown.addItems(["Male", "Female", "They/Them"])
        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(self.gender_dropdown)

        #Dm message chat box
        self.dm_message = QTextEdit()
        self.dm_message.setReadOnly(True)
        layout.addWidget(QLabel("DM:"))
        layout.addWidget(self.dm_message)

        #Users message area    Could later change user to character name
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your message here")
        layout.addWidget(QLabel("You:"))
        layout.addWidget(self.user_input)

        #send button
        self.send_button = QPushButton("Send")
        layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_message)

        self.setLayout(layout)

    def send_message(self):
        """
            Function to allow message back and forth to ai, allows no
            message to be sent as well and will still receive a reply.
        """
        system_prompt = "You are a creative Dungeon Master for a fantasy RPG."
        user_text = self.user_input.text()
        if user_text.strip():
            self.dm_message.append(f"<b>You:</b> {user_text}")
        response = self.ai_handler.get_ai_response(system_prompt, user_text)
        self.dm_message.append(f"<b>DM:</b> {response}")
        self.user_input.clear()
