# dnd-ai-dm

This project is for Green River College's course SDEV 450 Special Topics: AI and ML, Spring 2025 Final Project.

This repository holds a desktop app that has a user interface that allows any one player to interact with an AI dungeon master to play a roleplaying game.

## Technologies

This project uses the following technologies:

- [PyQT](https://pypi.org/project/PyQt6/) - Python Bindings to enable building a full stack application with only Python.
- [OpenRouterAI](https://openrouter.ai/) - Handles AI API calls.

## API Integration

All of our code handling the OpenRouter api endpoint is held within `ai_api_client.py` and our API key is set in the local .env file to prevent exposure.

Within our AIHandler class, we've defined the specific model and API url to use, along with a generalized method that takes in a system and user prompt, converts that to JSON, and sends that to the API for a response.

We save the API response locally and clean up the text before displaying it to the user in the front end.

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

## Project Structure

```
dnd-ai-dm/
├── app/                              # Holds all of our app's code
│   ├── main_window.py                # Our app's window
│   ├── logic                         # All backend code
│   │   ├── ai_api_client.py          # AI API interaction
│   │   ├── load_game.py              # Creates or loads a game
│   │   ├── process_game_input.py     # Handles all user inputs
│   │   └── save_load_data.py         # Saves and loads information to a local file
│   ├── resources                     # All app artifacts
│   │   └── saved_history             # Player, world, and chat information
│   │       ├── chat_history.json     # Chat history
│   │       ├── player.json           # Player and character details
│   │       └── world.json            # World lore
│   ├── views/
│   │   ├── app_view.py               # The main app's UI
│   │   └── welcome_view.py           # The welcome UI
│   └── widgets/
│       ├── character_form_widget.py  # Character form UI
│       ├── dm_chat_widget.py         # Chat history UI
│       ├── lore_widget.py            # Lore UI
│       └── user_input_widget.py      # User input UI
├── .env (.env.example)               # Environment key/values
├── main.py                           # Main entry point for the app
├── README.md
└── requirements.txt                  # Technical dependencies for the app
```

## Analysis - Capabilities and Limitations

We found it easy to design an intuitive player experience but found it difficult to get the AI model we chose to generate responses based on clear historical actions. We'll list the capablities and limitations of our app to demonstrate where our app succeeds and where it could improve.

### Capabilities

- The app takes in, saves, and retrieves the player name along with character details.
- The app uses AI to generate a new fantasy world (world, kingdoms, towns, NPCs) that the player can explore and saves this information locally for access.
- The app displays a blurb about the world so that the player can always refresh their memory about the world's lore.
- The game saves all user and AI interactions to a local file.
- The app sends historical game context along with user inputs to the AI in order to generate next steps/stories.
- AI is used to generate responses to user inputs and historical chat, which is then shown in the user interface as part of the chat log as the DM.

### Limitations

- The AI has a poor memory of historical context, which can lead to circular story telling.
- There is no way for the user to load their user profile, created character, or game world.

## Potential Future Improvements

- Use the player's name to find and load their character and game.
- The game can take user input on what type of game they want to play (background, setting, genre, etc).
- Use different LLM models and explore which ones give a better response/retain better historical context.
- Add in a multiplayer feature to support more than one player.
