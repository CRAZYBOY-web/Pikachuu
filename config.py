import os

# Required configurations (loaded from environment variables)
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "Cluster0")

# Owner and bot details
OWNER_ID = int(os.getenv("OWNER_ID", 0))
BOT_USERNAME = os.getenv("BOT_USERNAME", "PikachuuX_Bot")

# Links and visuals
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/+UhZo8ZsUECYyYWI1")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "https://t.me/pikachuu_updates")
START_IMAGE = os.getenv("START_IMAGE", "https://files.catbox.moe/bfalkz.jpg")
