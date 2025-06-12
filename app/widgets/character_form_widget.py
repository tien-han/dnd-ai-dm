# app/widgets/character_form_widget.py

"""
    This module is a form widget where the user can enter in
    their character preferences.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox

class CharacterFormWidget(QWidget):
    """Creates a form for the user to enter in their player characteristics."""

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.name_input = QLineEdit()
        self.race_dropdown = QComboBox()
        self.class_dropdown = QComboBox()
        self.gender_dropdown = QComboBox()

        self.init_ui()

    def init_ui(self):
        """Define and create our layout for the character form."""
        layout = QVBoxLayout()

        # Welcome message
        welcome_message = QLabel(
            f"Hello, {self.name}! Now choose your character info!" if self.name else "Hello!"
        )
        welcome_message.setStyleSheet("font-size: 20px; color: green")
        layout.addWidget(welcome_message)

        # Name
        layout.addWidget(QLabel("Character Name:"))
        self.name_input.setPlaceholderText("Enter your character name")
        layout.addWidget(self.name_input)

        # Race
        layout.addWidget(QLabel("Race:"))
        self.race_dropdown.addItems(["Human", "Dwarf", "Elf"])
        layout.addWidget(self.race_dropdown)

        # Class
        layout.addWidget(QLabel("Class:"))
        self.class_dropdown.addItems(["Fighter", "Mage", "Rogue"])
        layout.addWidget(self.class_dropdown)

        # Gender
        layout.addWidget(QLabel("Gender:"))
        self.gender_dropdown.addItems(["Male", "Female", "They/Them"])
        layout.addWidget(self.gender_dropdown)

        self.setLayout(layout)

    def get_character_info(self):
        """Makes the form selections available."""
        return {
            "player_name": self.name,
            "name": self.name_input.text(),
            "race": self.race_dropdown.currentText(),
            "class": self.class_dropdown.currentText(),
            "gender": self.gender_dropdown.currentText(),
        }
