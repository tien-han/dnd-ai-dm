# main.py

"""This is the entry point of the application."""

import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow

def main():
    """Starts and launches the application."""

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Start the event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
