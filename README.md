# TranslationBot

## Overview
TranslationBot is a Telegram bot that translates text between English and Persian. It supports:
- Full text translation
- Single-word translation with part-of-speech information and IPA pronunciation
- Secure access control based on allowed user IDs
- Deployment via Docker and Docker Compose

## Features
- **Language Translation:** Translates text between English and Persian using Google's Gemini API.
- **Word Analysis:** Provides part-of-speech and IPA pronunciation for English words.
- **User Access Control:** Only allowed users can use the bot.
- **Docker Support:** Easily deployable with Docker and Docker Compose.

## Project Structure
```
📦 TranslationBot
├─ .gitignore
├─ Dockerfile
├─ LICENSE
├─ docker-compose.yml
├─ example.env
├─ main.py
└─ requirements.txt
```

### File Descriptions
- `main.py`: The core script for the bot, handling translation and user interactions.
- `requirements.txt`: Lists Python dependencies.
- `Dockerfile`: Defines the Docker container setup.
- `docker-compose.yml`: Configuration for deploying with Docker Compose.
- `example.env`: Example environment variable file for configuration.
- `.gitignore`: Specifies files to exclude from version control.
- `LICENSE`: Specifies the project's license.

## Installation
### Prerequisites
- Python 3.8+
- A Telegram bot token from [BotFather](https://t.me/BotFather)
- A Google API key for Gemini

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/SajjadTalks/TranslationBot.git
   cd TranslationBot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file:
   ```bash
   cp example.env .env
   ```
4. Edit `.env` and set:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   GOOGLE_API_KEY=your_google_api_key
   MODELAI=gemini-pro  # or another supported model
   ALLOWED_USER_IDS=123456789,987654321  # Comma-separated Telegram user IDs
   ```

## Running the Bot
### Local Execution
Run the bot using:
```bash
python main.py
```

### Docker Deployment
1. Build the Docker image:
   ```bash
   docker build -t translationbot .
   ```
2. Run the container:
   ```bash
   docker run --env-file .env translationbot
   ```

### Docker Compose Deployment
1. Update `.env` with your credentials.
2. Start the bot:
   ```bash
   docker-compose up -d
   ```

## Usage
1. Start the bot by sending `/start`.
2. Send any text to translate.
3. The bot automatically detects the language and translates accordingly.
4. For single-word translations, it provides:
   - Part of speech
   - IPA pronunciation (for English words)
   - Example sentences in both languages

## License
This project is licensed under the Apache-2.0 License. See [LICENSE](LICENSE) for details.

## Author
[SajjadTalks](https://github.com/SajjadTalks)

## Contribution
Feel free to submit issues or pull requests to improve the bot!

