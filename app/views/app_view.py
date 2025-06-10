# app/views/app_view.py

"""This module defines the UI components that go into our main app page."""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QTextEdit, QPushButton


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

        #Character name input
        self.Character_name_input = QLineEdit()
        self.Character_name_input.setPlaceholderText("Enter your character name")
        layout.addWidget(QLabel("Character Name:"))
        layout.addWidget(self.Character_name_input)

        #Character Race dropdown
        self.race_dropdown = QComboBox()
        self.race_dropdown.addItems(["Human" , "Dwarf" , "Elf"])
        layout.addWidget(QLabel("Race:"))
        layout.addWidget(self.race_dropdown)

        #Character Class dropdown
        self.class_dropdown = QComboBox()
        self.class_dropdown.addItems(["Fighter", "Mage", "Rogue"])
        layout.addWidget(QLabel("Class:"))
        layout.addWidget(self.class_dropdown)

        #Character Gender Dropdown
        self.gender_dropdown = QComboBox()
        self.gender_dropdown.addItems(["Male", "Female", "They/Them"])
        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(self.gender_dropdown)

        #Dm message chat box
        self.dm_message = QTextEdit()
        self.dm_message.setReadOnly(True)
        layout.addWidget(QLabel("DM:"))
        layout.addWidget(self.dm_message)






        self.setLayout(layout)