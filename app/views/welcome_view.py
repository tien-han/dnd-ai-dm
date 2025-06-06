# app/views/main_window_view.py

"""This module defines the UI components that go into our welcome page."""

from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)

class WelcomeView(QWidget):
    """
        Define the layout for our welcome page and forward the user's entered
        name to our app.
    """

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Define our welcome message
        message = QLabel("🎉 Welcome to our AI DM Application! 🎉")
        message.setStyleSheet("font-size: 20px; color: green")

        # Widgets for asking the user for their name
        self.label = QLabel("Enter your name:")
        self.input = QLineEdit()
        self.button = QPushButton("Submit")

        # Connect the input field and submit button signal
        self.input.returnPressed.connect(self.handle_name_submit)
        self.button.clicked.connect(self.handle_name_submit)

        # Add widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        # Set the layout in the view
        self.setLayout(layout)

    def handle_name_submit(self):
        """Send the user's cleaned up name to our main app."""
        name = self.input.text().strip()
        self.main_window.show_app_view(name)
