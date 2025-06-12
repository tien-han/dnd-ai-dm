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

    def save_character(self, character_data):
        """Save the character information the user has created."""
        LOG.info("Processing the character form submission.")

        self.file_handler.save_player(character_data)

    def create_initial_scene(self, kingdom, town, character, race, user_class, gender):
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
            Then describes where they start and what they see around them.
        """
        world_info = f"""
            World: {self.world_data}
            Kingdom: {self.world_data["kingdoms"][kingdom]}
            Town: {self.world_data["kingdoms"][kingdom][town]}
            Your Character: {character}
            Your Race: {race}
            Your Class: {user_class}
            Your Gender: {gender}
            Your Start:
        """

        response = self.ai_handler.get_ai_response(system_prompt, world_info)
        LOG.info("Created initial story start:\n%s", response)
