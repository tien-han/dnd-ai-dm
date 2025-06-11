# app/views/main_window_view.py

"""This module defines the UI components that go into our welcome page."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)

class WelcomeView(QWidget):
    """
        Define the layout for our welcome page and forward the user's entered
        name to our app.
    """

    # Custom signal that emits the name string
    name_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Define our welcome message
        self.welcome_message = QLabel("🎉 Welcome to our AI DM Application! 🎉")
        self.welcome_message.setStyleSheet("font-size: 20px; color: green")

        # Widgets for asking the user for their name
        self.label = QLabel("Enter your name:")
        self.input = QLineEdit()
        self.button = QPushButton("Submit")

        self._init_ui()

    def _init_ui(self):
        """Load all our PyQT UI components."""
        self._setup_layout()
        self._connect_signals()

    def _setup_layout(self):
        """Add widgets to the layout on the welcome page."""
        layout = QVBoxLayout()

        # Add widgets to the layout
        layout.addWidget(self.welcome_message)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        # Set the layout in the view
        self.setLayout(layout)

    def _connect_signals(self):
        """Connect all PyQT signals on the welcome page."""
        # Connect the input field and submit button signal
        self.input.returnPressed.connect(self.handle_name_submit)
        self.button.clicked.connect(self.handle_name_submit)

    def handle_name_submit(self):
        """Attach the submitted name to our signal."""
        name = self.input.text().strip()
        if name:
            self.name_submitted.emit(name)
