# app/views/app_view.py

"""This module defines the UI components that go into our main app page."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QTextEdit, QPushButton
)
from app.logic import AIHandler, LoadGame
from charset_normalizer.cd import characters_popularity_compare
from datetime import datetime

class AppView(QWidget):
    """
        Defines our main app view.
    """

    def __init__(self, name: str):
        super().__init__()
        self.ai_handler = AIHandler()
        self.world_data = LoadGame().get_world_data()

        message = QLabel(f"Hello, {name}! Now choose your character info!" if name else "Hello!")
        message.setStyleSheet("font-size: 20px; color: green")

        self.layout = QVBoxLayout()
        self.layout.addWidget(message)

        #character form grouping
        self.character_form_widget = QWidget()
        character_form_layout = QVBoxLayout()


        #Character name input
        self.character_name_input = QLineEdit()
        self.character_name_input.setPlaceholderText("Enter your character name")
        character_form_layout.addWidget(QLabel("Character Name:"))
        character_form_layout.addWidget(self.character_name_input)

        #Character Race dropdown
        self.race_dropdown = QComboBox()
        self.race_dropdown.addItems(["Human" , "Dwarf" , "Elf"])
        character_form_layout.addWidget(QLabel("Race:"))
        character_form_layout.addWidget(self.race_dropdown)

        #Character Class dropdown
        self.class_dropdown = QComboBox()
        self.class_dropdown.addItems(["Fighter", "Mage", "Rogue"])
        character_form_layout.addWidget(QLabel("Class:"))
        character_form_layout.addWidget(self.class_dropdown)

        #Character Gender Dropdown
        self.gender_dropdown = QComboBox()
        self.gender_dropdown.addItems(["Male", "Female", "They/Them"])
        character_form_layout.addWidget(QLabel("Gender:"))
        character_form_layout.addWidget(self.gender_dropdown)

        self.character_form_widget.setLayout(character_form_layout)
        self.layout.addWidget(self.character_form_widget)


        #Dm message chat box
        self.dm_message = QTextEdit()
        self.dm_message.setReadOnly(True)
        self.layout.addWidget(QLabel("Game:"))
        self.layout.addWidget(self.dm_message)

        #Users message area    Could later change user to character name
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your message here")
        self.layout.addWidget(QLabel("You:"))
        self.layout.addWidget(self.user_input)

        #send button
        self.send_button = QPushButton("Send")
        self.layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_message)

        self.setLayout(self.layout)

    def send_message(self):
        """
            Function to allow message back and forth to ai, allows no
            message to be sent as well and will still receive a reply.
        """
        character_name = self.character_name_input.text()
        character_race = self.race_dropdown.currentText()
        character_class = self.class_dropdown.currentText()
        character_gender = self.gender_dropdown.currentText()
        user_text = self.user_input.text()
        if user_text.strip():
            full_user_message = (
                f"{character_name} ({character_race} {character_class}, {character_gender}) says: {user_text}"
            )
            self.dm_message.append(f"<b>You:</b> {full_user_message}")
        else:
            full_user_message = (
                f"{character_name} ({character_race} {character_class}, {character_gender}) is waiting silently..."
            )
        user_entry = {
            "role": "user",
            "message": full_user_message,
            "timestamp": datetime.now().isoformat()
        }
        system_prompt = "You are a creative Dungeon Master for a fantasy RPG."
        if self.character_form_widget.isVisible():
            self.character_form_widget.hide()
        response = self.ai_handler.get_ai_response(system_prompt, full_user_message)
        self.dm_message.append(f"<b>DM:</b> {response}")
        dm_entry = {
            "role": "dm",
            "message": response,
            "timestamp": datetime.now().isoformat()
        }
        self.user_input.clear()
