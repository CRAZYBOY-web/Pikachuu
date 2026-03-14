import os
from dotenv import load_dotenv

# Load variables from a .env file if it exists (for local testing)
load_dotenv()

class Config:
    # --- REQUIRED ---
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    MONGO_URL = os.environ.get("MONGO_URL", None)

    # --- CHANNELS & GROUPS ---
    SUPPORT_GRP = "UhZo8ZsUECYyYWI1" # Your support link hash
    UPDATE_CHNL = "pikachuu_updates"
    
    # --- BOT SETTINGS ---
    BOT_NAME = "༒ ᴘɪᴋᴀᴄʜᴜᴜ ༒"
    START_IMG = "https://telegra.ph/file/your_image_id.jpg" # Optional: Link to a logo
