import os
import asyncio
from pyrogram import Client, filters

# Get bot token and API credentials from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Initialize the bot
app = Client("rename_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Handle incoming files
@app.on_message(filters.document | filters.video | filters.photo)
async def rename_file(client, message):
    if not message.document and not message.video and not message.photo:
        return
    
    await message.reply("Send me the new filename (without extension):")
    
    response = await client.listen(message.chat.id)
    new_filename = response.text
    
    ext = message.document.file_name.split('.')[-1] if message.document else "mp4"
    
    file_path = await message.download()
    new_path = f"{new_filename}.{ext}"
    
    os.rename(file_path, new_path)

    await message.reply_document(new_path, caption="Here is your renamed file!")
    
    os.remove(new_path)

# Start the bot
app.run()