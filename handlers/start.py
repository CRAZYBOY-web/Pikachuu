# handlers/start.py

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    InputMediaPhoto
)
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db

# ==========================================================
# ʜᴇʟᴘᴇʀ: sᴇɴᴅ sᴛᴀʀᴛ ᴍᴇɴᴜ
# ==========================================================
async def send_start_menu(message, user_name):
    text = f"""
✨ **ʜᴇʟʟᴏ {user_name}!** ✨

👋 **ɪ ᴀᴍ ༒ ᴘɪᴋᴀᴄʜᴜᴜ ༒** ⚡️

**ʜɪɢʜʟɪɢʜᴛs:**
─────────────────────────────
- 🛡️ sᴍᴀʀᴛ ᴀɴᴛɪ-sᴘᴀᴍ & ʟɪɴᴋ sʜɪᴇʟᴅ
- ⚙️ ᴀᴅᴀᴘᴛɪᴠᴇ ʟᴏᴄᴋ sʏsᴛᴇᴍ (ᴜʀʟs, ᴍᴇᴅɪᴀ)
- 💎 ᴍᴏᴅᴜʟᴀʀ & sᴄᴀʟᴀʙʟᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ
- ⚡ sʟᴇᴇᴋ ᴜɪ ᴡɪᴛʜ ɪɴʟɪɴᴇ ᴄᴏɴᴛʀᴏʟs

» *ᴍᴏʀᴇ ɴᴇᴡ ꜰᴇᴀᴛᴜʀᴇs ᴄᴏᴍɪɴɢ sᴏᴏɴ ...*
"""
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚒️ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⚒️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("✨ sᴜᴘᴘᴏʀᴛ", url=SUPPORT_GROUP),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=UPDATE_CHANNEL),
        ],
        [
            InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", url=f"tg://user?id={OWNER_ID}"),
            InlineKeyboardButton("📂 ʀᴇᴘᴏ", url="https://github.com/LearningBotsOfficial/Nomade"),
        ],
        [InlineKeyboardButton("📚 ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs 📚", callback_data="help")]
    ])

    # Check if we should reply (new message) or edit (callback)
    if hasattr(message, 'from_user') and not hasattr(message, 'data'):
        await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)
    else:
        # Edit existing message media
        await message.edit_message_media(
            InputMediaPhoto(media=START_IMAGE, caption=text),
            reply_markup=buttons
        )

# ==========================================================
# sᴛᴀʀᴛ ᴄᴏᴍᴍᴀɴᴅ
# ==========================================================
@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    user = message.from_user
    await db.add_user(user.id, user.first_name)
    await send_start_menu(message, user.first_name)

# ==========================================================
# ʜᴇʟᴘ ᴍᴇɴᴜ
# ==========================================================
@Client.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query):
    text = """
╔══════════════════╗
      **ʜᴇʟᴘ ᴍᴇɴᴜ**
╚══════════════════╝

ᴄʜᴏᴏsᴇ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴄᴏᴍᴍᴀɴᴅs:
─────────────────────────────
"""
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👋 ɢʀᴇᴇᴛɪɴɢs", callback_data="greetings"),
            InlineKeyboardButton("🔒 ʟᴏᴄᴋs", callback_data="locks"),
        ],
        [InlineKeyboardButton("👮 ᴍᴏᴅᴇʀᴀᴛɪᴏɴ", callback_data="moderation")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_start")]
    ])
    await callback_query.message.edit_message_media(
        InputMediaPhoto(media=START_IMAGE, caption=text),
        reply_markup=buttons
    )
    await callback_query.answer()

# ==========================================================
# ʙᴀᴄᴋ ᴛᴏ sᴛᴀʀᴛ
# ==========================================================
@Client.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback(client, callback_query):
    # Using first_name from the callback user
    await send_start_menu(callback_query.message, callback_query.from_user.first_name)
    await callback_query.answer()

# [REST OF YOUR CALLBACK FUNCTIONS (GREETINGS, LOCKS, MODERATION) STAY THE SAME]

# ==========================================================
# ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴀɴᴅs
# ==========================================================
@Client.on_message(filters.user(OWNER_ID) & filters.command("stats"))
async def stats_command(client, message):
    count = await db.get_stats()
    await message.reply_text(f"📊 **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{count}`")

@Client.on_message(filters.user(OWNER_ID) & filters.command("broadcast"))
async def broadcast_command(client, message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.**")
    
    users = await db.get_all_users()
    msg = await message.reply_text(f"⚡ **ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴛᴏ {len(users)} ᴜsᴇʀs...**")
    
    done = 0
    for user_id in users:
        try:
            await message.reply_to_message.copy(user_id)
            done += 1
        except:
            pass
    await msg.edit(f"✅ **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**\n**sᴇɴᴛ ᴛᴏ:** `{done}`")
