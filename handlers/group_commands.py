from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, ChatPrivileges
from pyrogram.enums import ChatMemberStatus
import db
import logging

# Setup Logging
logger = logging.getLogger(__name__)

# --- ʜᴇʟᴘᴇʀ ꜰᴜɴᴄᴛɪᴏɴs ---

async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

async def get_user_id(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    parts = message.text.split()
    if len(parts) > 1:
        user = parts[1]
        if user.isdigit(): return int(user)
        try:
            user_obj = await client.get_users(user)
            return user_obj.id
        except: return None
    return None

# --- ᴍᴏᴅᴇʀᴀᴛɪᴏɴ ᴄᴏᴍᴍᴀɴᴅs ---

@Client.on_message(filters.group & filters.command("ban"))
async def ban_user(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id): return
    uid = await get_user_id(client, message)
    if not uid: return await message.reply("⚠️ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴘʀᴏᴠɪᴅᴇ ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ.")
    await client.ban_chat_member(message.chat.id, uid)
    await message.reply("🚨 ᴜsᴇʀ ʙᴀɴɴᴇᴅ!")

@Client.on_message(filters.group & filters.command("unban"))
async def unban_user(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id): return
    uid = await get_user_id(client, message)
    await client.unban_chat_member(message.chat.id, uid)
    await message.reply("✅ ᴜsᴇʀ ᴜɴʙᴀɴɴᴇᴅ!")

@Client.on_message(filters.group & filters.command("mute"))
async def mute_user(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id): return
    uid = await get_user_id(client, message)
    await client.restrict_chat_member(message.chat.id, uid, ChatPermissions(can_send_messages=False))
    await message.reply("🔇 ᴜsᴇʀ ᴍᴜᴛᴇᴅ!")

@Client.on_message(filters.group & filters.command("unmute"))
async def unmute_user(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id): return
    uid = await get_user_id(client, message)
    await client.restrict_chat_member(message.chat.id, uid, ChatPermissions(
        can_send_messages=True, can_send_media_messages=True, 
        can_send_other_messages=True, can_add_web_page_previews=True))
    await message.reply("🔊 ᴜsᴇʀ ᴜɴᴍᴜᴛᴇᴅ!")

@Client.on_message(filters.group & filters.command("promote"))
async def promote_user(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id): return
    uid = await get_user_id(client, message)
    await client.promote_chat_member(message.chat.id, uid, ChatPrivileges(
        can_manage_chat=True, can_delete_messages=True, can_restrict_members=True,
        can_invite_users=True, can_pin_messages=True, can_promote_members=True))
    await message.reply("✅ ᴘʀᴏᴍᴏᴛᴇᴅ ᴛᴏ ᴀᴅᴍɪɴ!")

# --- ʟᴏᴄᴋ sʏsᴛᴇᴍ ---

@Client.on_message(filters.group & filters.command("lock"))
async def lock_cmd(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id): return
    parts = message.text.split()
    if len(parts) < 2: return await message.reply("⚙️ ᴜsᴀɢᴇ: /ʟᴏᴄᴋ <ᴜʀʟ|sᴛɪᴄᴋᴇʀ|ᴍᴇᴅɪᴀ>")
    ltype = parts[1].lower()
    await db.set_lock(message.chat.id, ltype, True)
    await message.reply(f"🔒 {ltype.capitalize()} ʟᴏᴄᴋᴇᴅ.")

@Client.on_message(filters.group & ~filters.service, group=1)
async def enforce_locks(client, message):
    if await is_admin(client, message.chat.id, message.from_user.id): return
    locks = await db.get_locks(message.chat.id)
    if locks.get("url") and message.entities:
        for entity in message.entities:
            if entity.type in ["url", "text_link"]:
                await message.delete()
                return
    if locks.get("sticker") and message.sticker: await message.delete()
