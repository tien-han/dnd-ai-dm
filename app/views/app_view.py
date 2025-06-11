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

        #Users message area
        self.user_input_label = QLabel("You:")
        self.user_input_label.hide()
        self.layout.addWidget(self.user_input_label)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your message here")
        self.user_input.hide()
        self.layout.addWidget(self.user_input)

        #send button
        self.send_button = QPushButton("Send")
        self.layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_message)

        self.setLayout(self.layout)
        self.adventure_started = False
        self.world_intro_sent = False

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
        if not self.world_intro_sent:
            self.character_form_widget.hide()
            self.user_input_label.show()
            self.user_input.show()
            world_name = self.world_data.get("name", "Unknown World")
            world_description = self.world_data.get("description", "No description.")

            first_kingdom = next(iter(self.world_data.get("kingdoms", {}).values()), {})
            kingdom_name = first_kingdom.get("name", "Unknown Kingdom")
            kingdom_description = first_kingdom.get("description", "No description.")

            first_town = next(iter(first_kingdom.get("towns", {}).values()), {})
            town_name = first_town.get("name", "Unknown Town")
            town_description = first_town.get("description", "No description.")

            self.lore_text = QTextEdit()
            self.lore_text.setReadOnly(True)
            self.lore_text.setPlainText(
                f"🌍 World: {world_name}\n"
                f"{world_description}\n\n"
                f"🏰 Kingdom: {kingdom_name}\n"
                f"{kingdom_description}\n\n"
                f"🏘️ Town: {town_name}\n"
                f"{town_description}\n\n"
            )
            self.layout.insertWidget(1, self.lore_text)
            world_intro = (
                f"Welcome to the world of {world_name}.\n"
                f"You find yourself in the kingdom of {kingdom_name}.\n, "
                f"near the town of {town_name}.\n"
                f"What would you like to do?"
            )
            self.dm_message.append(f"<b>DM:</b> {world_intro}")
            self.world_intro_sent = True
        if not user_text.strip():
            return

        response = self.ai_handler.get_ai_response(system_prompt, full_user_message)
        self.dm_message.append(f"<b>DM:</b> {response}")
        dm_entry = {
            "role": "dm",
            "message": response,
            "timestamp": datetime.now().isoformat()
        }
        self.user_input.clear()

