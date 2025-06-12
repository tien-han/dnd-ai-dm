# app/widgets/user_input_widget.py

"""This module is used to handle user inputs."""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton

class UserInputWidget(QWidget):
    """
        Creates a user input widget where the user can enter in
        text and submit their responses.
    """
    def __init__(self):
        super().__init__()

        self.input_label = QLabel("You:")
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter your message here")
        self.send_button = QPushButton("Send")

        self.init_ui()

    def init_ui(self):
        """Defines the user input UI components and initial state."""
        layout = QHBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

        # Hide label/input initially
        self.input_label.hide()
        self.text_input.hide()

    def show_input_area(self):
        """Show the user text box and label."""
        self.input_label.show()
        self.text_input.show()

    def clear(self):
        """Clear the user's written text from the message box."""
        self.text_input.clear()

    def get_input_text(self) -> str:
        """Returns the user's written text."""
        return self.text_input.text().strip()
