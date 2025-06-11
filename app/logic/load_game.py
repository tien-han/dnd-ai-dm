# app/logic/load_game.py

"""This module loads the game into the application."""

import logging
import re
from .ai_api_client import AIHandler
from .save_load_data import FileSaverAndLoader

LOG = logging.getLogger(__name__)

class LoadGame():
    """Loads our game if it exists, creates it if not."""

    def __init__(self):
        self.ai_handler = AIHandler()
        self.file_handler = FileSaverAndLoader()
        self.world_data = {}
        self.system_prompt = """
            Your job is to help create interesting fantasy worlds that
            players would love to play in.
            Instructions:
            - Only generate in plain text without formatting.
            - Use simple clear language without being flowery.
            - You must stay below 3-5 sentences for each description.
        """

    def get_world_data(self):
        """Get world data if it already exists."""
        LOG.info("Attempting to get world data...")

        world_data = self.file_handler.load_world()

        if world_data is None or world_data.get("name") is None:
            LOG.info("There wasn't any world data, proceeding to generate.")
            world_data = self.generate_world()
        else:
            LOG.info("Existing world data: %s", world_data)

        self.world_data = world_data
        return self.world_data

    def generate_world(self):
        """Generate our initial world and save it locally to retain context."""
        LOG.info("Generating world...")

        self.create_world()
        self.create_kingdoms()
        self.create_towns()
        self.create_npcs()

        self.file_handler.save_world(self.world_data)

        return self.get_world_data()

    def create_world(self):
        """Defines initial context and creates our world at a high level."""
        LOG.info("Creating our world and setting.")

        world_prompt = """
            Generate a creative description for a unique fantasy world with an
            interesting concept around cities build on the backs of massive beasts.

            Output content in the form:
            World Name: <WORLD NAME>
            World Description: <WORLD DESCRIPTION>

            World Name:
        """

        response = self.ai_handler.get_ai_response(self.system_prompt, world_prompt)
        LOG.info("Generated world information was %s:", response)

        # Clean up response for saving and retrieving
        response_lines = response.splitlines()
        world_name = None
        world_description = None
        for line in response_lines:
            if line.startswith("World Name:"):
                world_name = line.replace("World Name:", "").strip()
            elif line.startswith("World Description:"):
                world_description = line.replace("World Description:", "").strip()

        self.world_data["name"] = world_name
        self.world_data["description"] = world_description

    def create_kingdoms(self):
        """Defines and creates kingdoms for our world."""
        LOG.info("Creating our kingdoms.")

        kingdom_prompt = f"""
            Create 3 different kingdoms for a fantasy world.
            For each kingdom generate a description based on the world it's in.
            Describe important leaders, cultures, history of the kingdom.

            Output content in the form:
            Kingdom 1 Name: <KINGDOM NAME>
            Kingdom 1 Description: <KINGDOM DESCRIPTION>
            Kingdom 2 Name: <KINGDOM NAME>
            Kingdom 2 Description: <KINGDOM DESCRIPTION>
            Kingdom 3 Name: <KINGDOM NAME>
            Kingdom 3 Description: <KINGDOM DESCRIPTION>

            World Name: {self.world_data["name"]}
            World Description: {self.world_data["description"]}

            Kingdom 1"""

        response = self.ai_handler.get_ai_response(self.system_prompt, kingdom_prompt)
        LOG.info("Generated kingdom information was \n%s:", response)

        # Clean up response for saving and retrieving
        kingdoms = {}

        # Regex to catch all name and description pairs, covering cases where the AI
        # responds in markdown and plaintext
        pattern = (
            r"(?:\*\*)?Kingdom \d+ Name:(?:\*\*)?\s*(.+?)\n"
            r"(?:\*\*)?Kingdom \d+ Description:(?:\*\*)?\s*(.+?)(?=\n(?:\*\*)?Kingdom \d+ Name:|\Z)"
        )

        matches = re.findall(pattern, response, re.DOTALL)
        LOG.info(matches)

        for name, description in matches:
            kingdom = {
                "name": name,
                "description": description,
                "world": self.world_data["name"]
            }
            kingdoms[name] = kingdom
        LOG.info("Created kingdoms were: %s", kingdoms)

        self.world_data['kingdoms'] = kingdoms

    def create_towns(self):
        """Defines and creates towns for the kingdoms for our world."""
        LOG.info("Creating our towns.")

        for kingdom in self.world_data["kingdoms"].values():
            town_prompt = f"""
                Create 3 different towns for a fantasy kingdom abd world.
                Describe the region it's in, important places of the town,
                and interesting history about it.
                
                Output content in the form:
                Town 1 Name: <TOWN NAME>
                Town 1 Description: <TOWN DESCRIPTION>
                Town 2 Name: <TOWN NAME>
                Town 2 Description: <TOWN DESCRIPTION>
                Town 3 Name: <TOWN NAME>
                Town 3 Description: <TOWN DESCRIPTION>
                
                World Name: {self.world_data["name"]}
                World Description: {self.world_data["description"]}
                
                Kingdom Name: {kingdom['name']}
                Kingdom Description {kingdom['description']}
                
                Town 1 Name:"""

            response = self.ai_handler.get_ai_response(self.system_prompt, town_prompt)
            LOG.info("Generated town information was \n%s:", response)

            # Clean up response for saving and retrieving
            towns = {}

            # Regex to catch all name and description pairs, covering cases where the AI
            # responds in markdown and plaintext
            pattern = (
                r"(?:\*\*)?Town \d+ Name:(?:\*\*)?\s*(.+?)\n"
                r"(?:\*\*)?Town \d+ Description:(?:\*\*)?\s*(.+?)(?=\n(?:\*\*)?Town \d+ Name:|\Z)"
            )

            matches = re.findall(pattern, response, re.DOTALL)
            LOG.info("Towns:\n%s", matches)

            for name, description in matches:
                town = {
                    "name": name,
                    "description": description,
                    "world": self.world_data["name"]
                }
                towns[name] = town
            LOG.info("Created towns were: %s", towns)

            kingdom["towns"] = towns

    def create_npcs(self):
        """Defines and creates NPCs for the towns in each kingdom of our world."""
        LOG.info("Creating our NPCs.")

        for kingdom in self.world_data["kingdoms"].values():
            for town in kingdom["towns"].values():
                npc_prompt = f"""
                    Create 3 different characters based on the world, kingdom \
                    and town they're in. Describe the character's appearance and \
                    profession, as well as their deeper pains and desires. \
                    
                    Output content in the form:
                    Character 1 Name: <CHARACTER NAME>
                    Character 1 Description: <CHARACTER DESCRIPTION>
                    Character 2 Name: <CHARACTER NAME>
                    Character 2 Description: <CHARACTER DESCRIPTION>
                    Character 3 Name: <CHARACTER NAME>
                    Character 3 Description: <CHARACTER DESCRIPTION>
                    
                    World Name: {self.world_data["name"]}
                    World Description: {self.world_data["description"]}
                    
                    Kingdom Name: {kingdom['name']}
                    Kingdom Description: {kingdom['description']}
                    
                    Town Name: {town['name']}
                    Town Description: {town['description']}
                    
                    Character 1 Name:
                """

                response = self.ai_handler.get_ai_response(self.system_prompt, npc_prompt)
                LOG.info("Generated npc information was \n%s:", response)

                # Clean up response for saving and retrieving
                npcs = {}

                # Regex to catch all name and description pairs, covering cases where the AI
                # responds in markdown and plaintext
                pattern = (
                    r"(?:\*\*)?Character \d+ Name:(?:\*\*)?\s*(.+?)\n"
                    r"(?:\*\*)?Character \d+ Description:(?:\*\*)?\s*(.+?)(?=\n(?:\*\*)?Character \d+ Name:|\Z)"
                )

                matches = re.findall(pattern, response, re.DOTALL)
                LOG.info("NPCs:\n%s", matches)

                for name, description in matches:
                    npc = {
                        "name": name,
                        "description": description,
                        "world": self.world_data["name"],
                        "kingdom": kingdom["name"],
                        "town": town["name"]
                    }
                    npcs[name] = npc
                LOG.info("Created npcs were: %s", npcs)

                town["npcs"] = npcs
