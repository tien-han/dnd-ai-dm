# app/logic/save_to_file.py

"""This module writes information to local files."""

import json
import logging
import os
from datetime import datetime

LOG = logging.getLogger(__name__)

class FileSaverAndLoader:
    """
        FileSaver holds methods to save text/json to local files.
    """

    def __init__(self, save_dir="app/resources/saved_history"):
        LOG.info("Initializing FileSaver...")
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

        self.world_file = os.path.join(save_dir, "world.json")
        self.player_file = os.path.join(save_dir, "player.json")
        self.chat_file = os.path.join(save_dir, "chat_history.json")

    def save_world(self, world_data: dict):
        """Save initial world generation to a local file."""
        LOG.info("Saving our world.")

        world_data["timestamp"] = datetime.now().isoformat()

        with open(self.world_file, 'w', newline='', encoding='utf-8') as world_file:
            json.dump(world_data, world_file, indent=2)

    def load_world(self):
        """Returns world information in json format."""
        LOG.info("Loading our world.")

        if not os.path.exists(self.world_file) or os.path.getsize(self.world_file) == 0:
            return None
        with open(self.world_file, "r", encoding="utf-8") as world_file:
            return json.load(world_file)

    def save_player(self, player_info: dict):
        """Save the player's information to a local file."""
        LOG.info("Saving the player's information.")

        player_info["timestamp"] = datetime.now().isoformat()

        with open(self.player_file, 'w', newline='', encoding='utf-8') as player_file:
            json.dump(player_info, player_file, indent=2)

    def load_player(self):
        """Load player information from a local file."""
        LOG.info("Loading player information.")

        if not os.path.exists(self.player_file):
            return []
        with open(self.player_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_chat(self, role: str, message: str):
        """Save chat interactions to a local file."""
        LOG.info("Saving chat entry.")

        entry = {
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        history = []
        if os.path.exists(self.chat_file):
            with open(self.chat_file, "r", encoding="utf-8") as chat_file:
                history = json.load(chat_file)

        history.append(entry)

        with open(self.chat_file, "w", encoding="utf-8") as chat_file:
            json.dump(history, chat_file, indent=2)

    def load_chat_history(self):
        """Load chat interactions from a local file."""
        LOG.info("Loading chat history.")

        if not os.path.exists(self.chat_file):
            return []
        with open(self.chat_file, "r", encoding="utf-8") as f:
            return json.load(f)
