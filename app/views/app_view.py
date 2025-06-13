# app/views/app_view.py

"""This module defines the UI components that go into our main app page."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from app.logic import LoadGame, ProcessGameInput
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
            self.send_user_input()
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

    def send_user_input(self):
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

        # Create the user text to show in the chat history
        user_text = self.user_input.get_input_text() # Returns an empty string if there's no input.
        if user_text.strip():
            full_user_message = (
                f"{character_name} ({character_race} {character_class}, "
                f"{character_gender}) says: {user_text}"
            )
        else: # If the user didn't enter anything into the text box
            full_user_message = (
                f"{character_name} ({character_race} {character_class}, ",
                f"{character_gender}) is waiting silently..."
            )
        self.dm_chat.append_user_message(full_user_message)

        dm_response = self.process_input.get_dm_response(full_user_message)
        self.dm_chat.append_dm_message(dm_response)

        self.user_input.clear()
