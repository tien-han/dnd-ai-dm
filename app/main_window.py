# app/main_window.py

"""
    This module is the controller for our application.

    We define our root application window here and have methods that
    help route the user through different views.
"""

from PyQt6.QtWidgets import QMainWindow
from app.views import AppView, WelcomeView

class MainWindow(QMainWindow):
    """
        Defines our root application window, which includes the
        menu, toolbar, etc, along with methods that control
        navigation between each view.
    """

    def __init__(self):
        super().__init__()

        # Set the application settings
        self.setWindowTitle("Welcome to the AI DM Application")
        self.setMinimumSize(400, 200)

        # Start the app with the welcome page
        self.welcome_view = WelcomeView(self)
        self.setCentralWidget(self.welcome_view)

    def show_app_view(self, name: str):
        """
            Updates the view to our main application view once a user
            as entered their name.
        """

        self.setCentralWidget(AppView(name))
