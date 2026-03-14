import logging
from pyrogram import Client
from config import Config # Importing the Config class

# 1. Setup Logging (Very important for debugging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 2. Initialize the Client with variables from the Config class
app = Client(
    "PikachuuBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="handlers") # This automatically loads everything in /handlers
)

# 3. Execution Block
if __name__ == "__main__":
    logger.info("⚡ ༒ ᴘɪᴋᴀᴄʜᴜᴜ ༒ Is Starting...")
    try:
        app.run()
    except Exception as e:
        logger.error(f"❌ Boot failed: {e}")
