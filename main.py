import os
import re
from dotenv import load_dotenv
import telebot
import google.generativeai as genai

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODELAI")
ALLOWED_USER_IDS = os.getenv("ALLOWED_USER_IDS", "")  # Get allowed user IDs, default to empty string

# --- Validate Environment Variables ---
if not MODEL_NAME or not isinstance(MODEL_NAME, str):
    raise ValueError("MODELAI environment variable must be set to a valid model name string (e.g., 'gemini-pro').")

# Convert allowed user IDs to a set of integers
try:
    ALLOWED_USER_IDS = {int(user_id) for user_id in ALLOWED_USER_IDS.split(',') if user_id.strip()}
except ValueError:
    raise ValueError("ALLOWED_USER_IDS environment variable must be a comma-separated list of integers.")


# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# --- Gemini API Interaction ---

def translate_text(text: str, is_single_word: bool = False, to_persian: bool = True) -> str:
    """Translates text using Gemini, handling single words and direction."""
    try:
        if is_single_word:
            if to_persian:
                prompt = f"""
                You are a helpful translator and linguistic analyzer. Translate the following English word to Persian.
                Also, identify the word's part of speech (e.g., verb, noun, adjective).
                Provide the word's pronunciation using the International Phonetic Alphabet (IPA), enclosed in slashes.  Do NOT include any Persian transliterations, parentheses, or alternative Persian translations. Give ONLY ONE Persian translation.
                Provide a short example sentence in both English and Persian using the word. Do NOT include any Persian transliterations in the example sentences.

                Word: {text}

                Output in the following format (do NOT include any introductory text, ONLY the requested information):

                Translation: [Persian Translation]
                Part of Speech: [Part of Speech]
                IPA Pronunciation: [IPA Pronunciation]
                Example (EN): [English Example]
                Example (FA): [Persian Example]
                """
            else:  # Persian to English
                prompt = f"""
                You are a helpful translator and linguistic analyzer. Translate the following Persian word to English.
                Also, identify the word's part of speech (e.g., verb, noun, adjective).
                Provide a short example sentence in both Persian and English using the word. Do NOT include any transliterations.

                Word: {text}

                Output in the following format (do NOT include any introductory text, ONLY the requested information):

                Translation: [English Translation]
                Part of Speech: [Part of Speech]
                Example (FA): [Persian Example]
                Example (EN): [English Example]
                """

            response = model.generate_content(prompt)
            cleaned_response = response.text

            # Keep IPA pronunciation, but remove other unwanted parts.
            cleaned_response = re.sub(r'\(.*?\)', '', cleaned_response)
            cleaned_response = re.sub(r'\[(?!/).*?(?<!/)\]', '', cleaned_response)
            cleaned_response = re.sub(r'or\s*/[^/].*', '', cleaned_response)
            cleaned_response = cleaned_response.replace(":", ": ")
            return cleaned_response.strip()

        else:  # Multi-word
            if to_persian:
                prompt = f"""Translate the following text to Persian. Only provide the Persian translation, do not include any of the original English text or any explanations.

                Text:
                {text}
                """
            else:
                prompt = f"""Translate the following text to English. Only provide the English translation, do not include any of the original Persian text or explanations.

                Text:
                {text}
                """
            response = model.generate_content(prompt)
            return response.text.strip()

    except Exception as e:
        print(f"Error during translation: {e}")
        if "400" in str(e):
            return "Translation service is currently unavailable. Please try again later or check GOOGLE_API_KEY."
        return "An error occurred during translation. Please try again later."


# --- Telegram Bot Handlers (pyTelegramBotAPI) ---
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in ALLOWED_USER_IDS:
        bot.reply_to(message, "I'm a translator bot! Send me text in English or Persian, and I'll translate it. I can also handle single words and provide part of speech information and IPA pronunciation for English words.")
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

@bot.message_handler(func=lambda message: True, content_types=['text', 'sticker', 'document', 'photo', 'audio', 'video', 'voice', 'contact', 'location', 'venue', 'dice', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'web_app_data'])
def handle_all(message):
    # Check if the user is allowed
    if message.from_user.id not in ALLOWED_USER_IDS:
        bot.reply_to(message, "You are not authorized to use this bot.")
        return

    # Check if the message is a command other than /start
    if message.content_type == 'text' and message.text.startswith('/') and message.text != '/start':
        return  # Ignore other commands

    # Check if the message is NOT text
    if message.content_type != 'text':
        return  # Ignore non-text messages (stickers, GIFs, etc.)

    # If it's text and not another command, proceed with translation
    text = message.text
    words = text.split()
    is_single_word = len(words) == 1

    first_word = words[0]
    is_persian = any("\u0600" <= char <= "\u06FF" for char in first_word)
    to_persian = not is_persian

    translation = translate_text(text, is_single_word=is_single_word, to_persian=to_persian)
    bot.reply_to(message, translation)

def main():
    if not BOT_TOKEN or not GOOGLE_API_KEY:
        raise ValueError("Both BOT_TOKEN and GOOGLE_API_KEY must be set in the .env file.")
    print("Bot is running...")
    bot.polling()

if __name__ == '__main__':
    main()