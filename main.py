
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import logging

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the Client with the Plugins folder
app = Client(
    "pikachu_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers") # This automatically loads everything in the handlers folder
)

if __name__ == "__main__":
    print("⚡️ ༒ ᴘɪᴋᴀᴄʜᴜᴜ ༒ ɪs sᴛᴀʀᴛɪɴɢ... ")
    app.run()
