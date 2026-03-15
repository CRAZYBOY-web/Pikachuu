from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import logging

# ᴇɴᴀʙʟᴇ ʟᴏɢɢɪɴɢ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ɪɴɪᴛɪᴀʟɪᴢᴇ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜ ᴘʟᴜɢɪɴs
app = Client(
    "pikachu_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers") # ᴛʜɪs ᴀᴜᴛᴏ-ʟᴏᴀᴅs ᴇᴠᴇʀʏᴛʜɪɴɢ ɪɴ ᴛʜᴇ ʜᴀɴᴅʟᴇʀs ꜰᴏʟᴅᴇʀ
)

if __name__ == "__main__":
    print("⚡️ ༒ ᴘɪᴋᴀᴄʜᴜᴜ ༒ ɪs sᴛᴀʀᴛɪɴɢ... ")
    app.run()
