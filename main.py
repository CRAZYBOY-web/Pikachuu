from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

app = Client(
    "pikachu_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)

async def start_bot():
    await app.start()
    print("⚡️ ༒ ᴘɪᴋᴀᴄʜᴜᴜ ༒ ɪs ʟɪᴠᴇ!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
    
