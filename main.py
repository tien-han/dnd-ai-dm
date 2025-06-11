# main.py

"""This is the entry point of the application."""

import logging
import sys
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow

# Load environment variables
load_dotenv()
# Add in logging
LOG = logging.getLogger(__name__)

def main():
    """Starts and launches the application."""
    logging.basicConfig(
        filename='ai_dm_app.log',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    LOG.info("App is starting up")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Start the event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
