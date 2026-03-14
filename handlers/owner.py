import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from config import Config
import db

# --- OWNER ONLY STATS ---
@Client.on_message(filters.user(Config.OWNER_ID) & filters.command("stats"))
async def get_bot_stats(client, message: Message):
    count = await db.get_stats()
    await message.reply_text(f"📊 **ᴘɪᴋᴀᴄʜᴜᴜ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ sᴛᴀᴛs:**\n\n**ᴛᴏᴛᴀʟ ᴜsᴇʀs:** {count}")

# --- BROADCAST SYSTEM ---
@Client.on_message(filters.user(Config.OWNER_ID) & filters.command("broadcast"))
async def broadcast_msg(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.**")

    all_users = await db.get_all_users()
    msg = await message.reply_text(f"⚡ **ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛᴇᴅ...**\n**ᴛᴀʀɢᴇᴛ:** {len(all_users)} ᴜsᴇʀs")

    done = 0
    failed = 0
    
    for user_id in all_users:
        try:
            await message.reply_to_message.copy(user_id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(user_id)
            done += 1
        except (InputUserDeactivated, UserIsBlocked):
            failed += 1
        except Exception:
            failed += 1

    await msg.edit(f"✅ **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**\n\n**sᴇɴᴛ ᴛᴏ:** {done}\n**ꜰᴀɪʟᴇᴅ:** {failed}")
