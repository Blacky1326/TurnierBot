# Discord Tournament Bot

This project is a Discord bot designed to facilitate tournament management within Discord servers. It allows users to create, configure, and manage tournaments, as well as handle player registrations and leaderboards. The bot ensures that only users with the appropriate permissions can execute certain commands.

## Features

- Create and manage tournaments
- Player registration and management
- Leaderboard functionalities
- Admin-only commands to ensure proper permissions

## Project Structure

```
discord-tournament-bot
├── src
│   ├── bot.py                     # Entry point for the Discord bot
│   ├── commands
│   │   ├── __init__.py            # Initializes the commands package
│   │   └── tournament_commands.py   # Contains tournament-related commands
│   ├── utils
│   │   └── permissions.py          # Utility functions for permission checks
│   └── data                        # Directory for server-specific data
├── requirements.txt                # Lists project dependencies
└── README.md                       # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd discord-tournament-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a Discord bot and obtain your bot token from the Discord Developer Portal.

4. Replace `YOUR_BOT_TOKEN` in `src/bot.py` with your actual bot token.

5. Run the bot:
   ```
   python src/bot.py
   ```

## Command Usage

- `!create_tournament <name>`: Creates a new tournament with the specified name (admin only).
- `!register <player_name>`: Registers a player for the current tournament.
- `!start_tournament`: Starts the tournament (admin only).
- `!end_tournament`: Ends the current tournament and displays results (admin only).
- `!leaderboard`: Displays the current leaderboard for the tournament.

## Contribution Guidelines

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.