import os
from pyrogram import Client, filters, enums
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPrivileges, ChatPermissions

# --- CONFIG ---
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL")

app = Client("pikachuu_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = AsyncIOMotorClient(MONGO_URL).pikachuu_db
settings_db = db.settings
welcome_db = db.welcome

# --- HELPER: ADMIN CHECK ---
async def is_admin(chat_id, user_id):
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]

# --- 1. WELCOME SYSTEM (WITH CUSTOM SMS) ---
@app.on_message(filters.new_chat_members)
async def welcome_new_member(client, message):
    chat_id = message.chat.id
    custom_welcome = await welcome_db.find_one({"chat_id": chat_id})
    
    welcome_text = custom_welcome["text"] if custom_welcome else (
        f"❖ **Welcome to {message.chat.title}!** ⚡\n\n"
        "❖ I am **Pikachuu**, your protector. Please follow the rules!"
    )
    
    for member in message.new_chat_members:
        await message.reply_text(welcome_text.replace("{user}", member.mention))

@app.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome(client, message):
    if await is_admin(message.chat.id, message.from_user.id):
        welcome_msg = message.text.split(None, 1)[1] if len(message.command) > 1 else None
        if welcome_msg:
            await welcome_db.update_one({"chat_id": message.chat.id}, {"$set": {"text": welcome_msg}}, upsert=True)
            await message.reply_text("❖ **Custom Welcome Message Saved!**")

# --- 2. LOCK SYSTEM (MESSAGES/STICKERS) ---
@app.on_message(filters.command(["lock", "unlock"]) & filters.group)
async def lock_unlock(client, message):
    if not await is_admin(message.chat.id, message.from_user.id): return
    
    cmd = message.command[0]
    target = message.command[1] if len(message.command) > 1 else "all"

    if cmd == "lock":
        if target == "stickers":
            await client.set_chat_permissions(message.chat.id, ChatPermissions(can_send_other_messages=False))
            await message.reply_text("❖ **Stickers Locked!** 🚫")
        else:
            await client.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=False))
            await message.reply_text("❖ **Chat Locked!** 🔒")
    else:
        await client.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=True, can_send_other_messages=True))
        await message.reply_text("❖ **Everything Unlocked!** 🔓")

# --- 3. PROMOTE / DEMOTE ---
@app.on_message(filters.command(["promote", "fullpromote", "demote"]) & filters.group)
async def admin_manage(client, message):
    if not await is_admin(message.chat.id, message.from_user.id): return
    if not message.reply_to_message: return await message.reply_text("Reply to a user!")

    user_id = message.reply_to_message.from_user.id
    cmd = message.command[0]

    if cmd == "promote":
        await client.promote_chat_member(message.chat.id, user_id, ChatPrivileges(can_manage_chat=True, can_delete_messages=True, can_restrict_members=True))
        await message.reply_text("❖ User Promoted to Admin!")
    elif cmd == "fullpromote":
        await client.promote_chat_member(message.chat.id, user_id, ChatPrivileges(can_manage_chat=True, can_delete_messages=True, can_manage_video_chats=True, can_promote_members=True, can_restrict_members=True, can_pin_messages=True))
        await message.reply_text("❖ User Full Promoted! ⚡")
    elif cmd == "demote":
        await client.promote_chat_member(message.chat.id, user_id, ChatPrivileges())
        await message.reply_text("❖ User Demoted!")

# --- 4. HELP COMMAND ---
@app.on_message(filters.command("help"))
async def bot_help(client, message):
    help_text = (
        "**༒ ᴘɪᴋᴀᴄʜᴜᴜ ᴄᴏᴍᴍᴀɴᴅs ༒**\n\n"
        "❖ `/ban` / `/unban` - User Management\n"
        "❖ `/mute` / `/unmute` - Silence Users\n"
        "❖ `/promote` / `/demote` - Admin Roles\n"
        "❖ `/lock` / `/unlock` - Chat Control\n"
        "❖ `/id` / `/info` - User Stats\n"
        "❖ `/settings` - Toggle Protection\n"
        "❖ `/setwelcome` - Set Custom Greeting"
    )
    await message.reply_text(help_text)

# (Plus all the Ban, Mute, Info, Anti-Spam code we wrote previously)
app.run()
