# app/widgets/lore_widget.py

"""This module displays the world lore for the game."""

from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout

class LoreWidget(QWidget):
    """Widget to display world, kingdom, and town lore."""

    def __init__(self, world_data):
        super().__init__()
        self.world_data = world_data

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.layout.addWidget(self.text_box)

    def set_lore_text(self):
        """Fill the widget with lore information."""
        world_name = self.world_data.get("name", "Unknown World").strip()
        world_description = self.world_data.get("description", "No description.").strip()

        first_kingdom = next(iter(self.world_data.get("kingdoms", {}).values()), {})
        kingdom_name = first_kingdom.get("name", "Unknown Kingdom").strip()
        kingdom_description = first_kingdom.get("description", "No description.").strip()

        first_town = next(iter(first_kingdom.get("towns", {}).values()), {})
        town_name = first_town.get("name", "Unknown Town").strip()
        town_description = first_town.get("description", "No description.").strip()

        self.text_box.setPlainText(
            f"🌍 World: {world_name}\n"
            f"{world_description}\n\n"
            f"🏰 Kingdom: {kingdom_name}\n"
            f"{kingdom_description}\n\n"
            f"🏘️ Town: {town_name}\n"
            f"{town_description}"
        )
