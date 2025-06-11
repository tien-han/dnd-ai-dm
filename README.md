# dnd-ai-dm

This project is for Green River College's course SDEV 450 Special Topics: AI and ML, Spring 2025 Final Project.

This repository holds a desktop app that has a user interface that allows any one player to interact with an AI dungeon master to play a roleplaying game.

## Technologies

This project uses the following technologies:

- (PyQT)[https://pypi.org/project/PyQt6/] - Python Bindings to enable building a full stack application with only Python.

## Running the Project

Prior to running the project, you'll need to install:

- [Visual Studio Code ](https://code.visualstudio.com/)
- [Python](https://www.python.org/downloads/)

### Setup Environment and Dependencies

The following steps are done through the terminal.

1. Create and activate your Python virtual environment.

   ```
   # Create new env
   `python3 -m venv .venv`

   # Activate env
   source .venv/bin/activate

   # Confirm the env is up
   which python

   # Close out env when done running the project
   deactivate
   ```

   Note: After your first run, you only need to run the activate env command to start the virtual environment.

2. Install the project requirements (only needed on first run).

   ```
   # Install the requirements
   pip install --no-cache-dir -r requirements.txt
   ```

3. Copy the `.env.example` file and rename it to `.env`. Add in your API key in this file as OPENROUTER_API_KEY=sk-rest-of-api-key-here

### Start the project locally

While in the project root directory `dnd-ai-dm`, start the application with:

```
python3 main.py
```

You should see the application window pop up.

## Developing the Application

This section will go over how to make code changes in the application for a smooth experience.

### Adding a new View

1. Add your view to `app/views` as it's own file.
2. Update `app/views/__init__py` to include this new file in the views module.
3. Within `app/main_window.py`, import your view class name and add in a new method in the `MainWindow` class that will set the central widget to your new view.

## Troubleshooting

### Pylint errors with imports

If you have import errors like "No name 'QMainWindow' in module 'PyQt6.QtWidgets'", this is due to Pylint not automatically loading C extensions. The solution is to suppress these warnings by navigating to your VSCode Settings > Workspace > Extensions > Pylint and adding the line `--extension-pkg-whitelist=PyQt6` to the Pylint Args.

Alternatively, you can open `settings.json` and add in this code:

```
{
    "pylint.args": [
        "--extension-pkg-whitelist=PyQt6"
    ]
}
```
