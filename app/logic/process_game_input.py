# app/logic/process_game_input.py

"""This module handles user inputs and prepares them for sending to the AI model."""

import logging
from .ai_api_client import AIHandler
from .save_load_data import FileSaverAndLoader

LOG = logging.getLogger(__name__)

class ProcessGameInput():
    """Handles user inputs and ensures the AI model has full context."""

    def __init__(self, world_data):
        self.ai_handler = AIHandler()
        self.file_handler = FileSaverAndLoader()
        self.world_data = world_data
        self.world_info = None
        self.history = []
        self.character = None

    def save_character(self, character_data):
        """Save the character information the user has created."""
        LOG.info("Processing the character form submission.")
        self.character = character_data
        self.file_handler.save_player(character_data)

    def create_initial_scene(self, kingdom, town):
        """Create the initial scene for the game."""
        LOG.info("Creating initial story...")

        system_prompt = """
            You are an AI Game master. Your job is to create a 
            start to an adventure based on the world, kingdom, town and character 
            a player is playing as. 
            Instructions:
            You must only use 2-4 sentences
            Write in second person. For example: "You are Jack"
            Write in present tense. For example "You stand at..."
            First describe the character and their backstory.
            Then describe where they start and what they see around them.
        """
        self.world_info = f"""
            World: {self.world_data}
            Kingdom: {kingdom}
            Town: {town}
            Your Character: {self.character["name"]}
            Your Race: {self.character["race"]}
            Your Class: {self.character["class"]}
            Your Gender: {self.character["gender"]}
            Your Start:
        """

        response = self.ai_handler.get_ai_response(system_prompt, self.world_info)
        LOG.info("Created initial story start:\n%s", response)

        # Save the selected lore and the generated dialogue to the chat history
        self.file_handler.save_chat("info", self.world_info)
        self.file_handler.save_chat("dm", response)

        # Save to our history to send back to the llm
        self.history.append({"role": "user", "content": self.world_info})
        self.history.append({"role": "assistant", "content": response})

        return response

    def get_dm_response(self, user_message):
        """Send the user's written text to the AI model and return the DM response."""
        LOG.info("Sending the user's input to the AI model...")

        system_prompt = """
            You are an AI Game master. Your job is to write what
            happens next in a player's adventure game.
            Instructions:
            You must on only write 1-3 sentences in response.
            Always write in second person present tense.
            Ex. (You look north and see...)
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": self.world_info}
        ]
        # Add in the history of actions
        messages.extend(self.history)
        # Add in the message that user just added.
        messages.append({"role": "user", "content": user_message})

        response = self.ai_handler.get_ai_response(system_prompt, messages)
        LOG.info("Sent user input with action history and got AI DM response:")
        LOG.info(messages)
        LOG.info(response)

        self.file_handler.save_chat("user", user_message)
        self.file_handler.save_chat("dm", response)

        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": response})

        return response
