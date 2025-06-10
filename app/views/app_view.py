# app/views/app_view.py

"""This module defines the UI components that go into our main app page."""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox

class AppView(QWidget):
    """
        Defines our main app view.
    """

    def __init__(self, name: str):
        super().__init__()

        message = QLabel(f"Hello, {name}! Now choose your character info!" if name else "Hello!")
        message.setStyleSheet("font-size: 20px; color: green")

        layout = QVBoxLayout()
        layout.addWidget(message)


        self.Character_name_input = QLineEdit()
        self.Character_name_input.setPlaceholderText("Enter your character name")
        layout.addWidget(QLabel("Character Name:"))
        layout.addWidget(self.Character_name_input)

        self.race_dropdown = QComboBox()
        self.race_dropdown.addItems(["Human" , "Dwarf" , "Elf"])
        layout.addWidget(QLabel("Race:"))
        layout.addWidget(self.race_dropdown)





        self.setLayout(layout)