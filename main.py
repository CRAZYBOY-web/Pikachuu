import logging
from pyrogram import Client, filters
from config import Config
import db

# Setup Logging to see errors in the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class PikachuuBot(Client):
    def __init__(self):
        super().__init__(
            "Pikachuu_Protection",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="handlers") # This automatically loads all files in /handlers
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logger.info(f"✅ @{me.username} sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!")
        print(f"⚡ ᴘɪᴋᴀᴄʜᴜᴜ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ɪs ʟɪᴠᴇ!")

    async def stop(self, *args):
        await super().stop()
        logger.info("ᴘɪᴋᴀᴄʜᴜᴜ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ sᴛᴏᴘᴘᴇᴅ. ɢᴏᴏᴅʙʏᴇ!")

# --- AUTO-SAVE USERS TO DATABASE ---
# This ensures every person who starts the bot is added to your DB for /stats and /broadcast
@PikachuuBot.on_message(filters.private & filters.incoming, group=-1)
async def save_user_on_msg(client, message):
    await db.add_user(message.from_user.id, message.from_user.first_name)

if __name__ == "__main__":
    app = PikachuuBot()
    app.run()
