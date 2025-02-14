import os
import asyncio
import threading
from pyrogram import Client, filters
from flask import Flask

from flask import Flask

# Create a Flask application instance
app = Flask(_name_)

# Define a simple route
@app.route('/')
def home():
    return "Bot is running!"

# Ensure this runs only in development mode, not with Gunicorn
if _name_ == "_main_":
    app.run()
@app.route('/')
def home():
    return "Bot is running!"

# Run Flask in the background
def run_dummy_server():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Start Flask server in a separate thread
threading.Thread(target=run_dummy_server, daemon=True).start()

# Get bot token and API credentials from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Initialize the bot
bot = Client("rename_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Dictionary to store user file download paths
user_files = {}

@bot.on_message(filters.document | filters.video | filters.photo)
async def request_new_filename(client, message):
    if message.document:
        ext = message.document.file_name.split('.')[-1]
    elif message.video:
        ext = "mp4"
    else:  # Photo case
        ext = "jpg"

    file_path = await message.download()
    user_files[message.chat.id] = (file_path, ext)

    await message.reply("Send me the new filename (without extension):")

@bot.on_message(filters.text & filters.reply)
async def rename_and_send(client, message):
    chat_id = message.chat.id
    if chat_id not in user_files:
        await message.reply("No file found to rename. Please send a file first.")
        return

    new_filename = message.text.strip()
    file_path, ext = user_files.pop(chat_id)

    new_path = f"{new_filename}.{ext}"
    os.rename(file_path, new_path)

    await message.reply_document(new_path, caption="Here is your renamed file!")

    os.remove(new_path)

# Start the bot
bot.run()
