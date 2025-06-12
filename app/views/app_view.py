# app/views/app_view.py

"""This module defines the UI components that go into our main app page."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from app.logic import AIHandler, LoadGame, ProcessGameInput
from app.widgets import CharacterFormWidget, DMChatWidget, LoreWidget, UserInputWidget

class AppView(QWidget):
    """Defines the main app view."""

    def __init__(self, name: str):
        super().__init__()
        # Game Data
        self.world_data = LoadGame().get_world_data()
        self.adventure_started = False
        # Widgets
        self.character_form = CharacterFormWidget(name)
        self.dm_chat = DMChatWidget()
        self.lore_window = LoreWidget(self.world_data)
        self.user_input = UserInputWidget()
        # Handlers
        self.ai_handler = AIHandler()
        self.process_input = ProcessGameInput(self.world_data)

        # Add widgets to the UI layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.character_form)
        self.layout.addWidget(self.dm_chat)
        self.layout.addWidget(self.user_input)

        # Connect send button
        self.user_input.send_button.clicked.connect(self.handle_send_button)

        self.setLayout(self.layout)

    def handle_send_button(self):
        """Determines what to do when the send button is clicked."""
        if self.adventure_started:
            self.send_message()
        else:
            self.submit_form_and_update_page()
            self.get_starting_dialogue()
            self.adventure_started = True

    def submit_form_and_update_page(self):
        """Submit the initial character creation form."""
        # Save the player's information
        self.process_input.save_character(self.character_form.get_character_info())

        # Update the UI
        self.character_form.hide()
        self.user_input.show_input_area()
        self.lore_window.set_lore_text()
        self.layout.insertWidget(1, self.lore_window)

    def get_starting_dialogue(self):
        """Get and show the initial dialoge to start the game."""
        first_kingdom = next(iter(self.world_data.get("kingdoms", {}).values()), {})
        first_town = next(iter(first_kingdom.get("towns", {}).values()), {})
        starting_dialogue = self.process_input.create_initial_scene(first_kingdom, first_town)

        self.dm_chat.append_dm_message(starting_dialogue)

    def send_message(self):
        """
            Function to allow message back and forth to ai, allows no
            message to be sent as well and will still receive a reply.
        """
        # Get the player's character information
        character_info = self.character_form.get_character_info()
        character_name = character_info["name"]
        character_race = character_info["race"]
        character_class = character_info["class"]
        character_gender = character_info["gender"]

        user_text = self.user_input.get_input_text()
        if user_text.strip():
            full_user_message = (
                f"{character_name} ({character_race} {character_class}, {character_gender}) says: {user_text}"
            )
            self.dm_chat.append_user_message(full_user_message)
        else:
            full_user_message = (
                f"{character_name} ({character_race} {character_class}, {character_gender}) is waiting silently..."
            )
        user_entry = {
            "role": "user",
            "message": full_user_message
        }
        system_prompt = "You are a creative Dungeon Master for a fantasy RPG."

        if not user_text.strip():
            return

        response = self.ai_handler.get_ai_response(system_prompt, full_user_message)
        self.dm_chat.append_dm_message(response)
        dm_entry = {
            "role": "dm",
            "message": response
        }
        self.user_input.clear()
