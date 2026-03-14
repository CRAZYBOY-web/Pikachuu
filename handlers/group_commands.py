
from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, ChatPermissions, ChatPrivileges
from pyrogram.enums import ChatMemberStatus
import logging
import db  # Ensure your db.py has the functions used here

DEFAULT_WELCOME = "👋 Welcome {first_name} to {title}!"

logger = logging.getLogger(__name__)

# ==========================================================
# POWER LOGIC (Admin Check)
# ==========================================================
async def is_power(client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception:
        return False

async def extract_target_user(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return None
    arg = parts[1]
    try:
        if arg.startswith("@"):
            return await client.get_users(arg)
        elif arg.isdigit():
            return await client.get_users(int(arg))
    except Exception:
        return None
    return None

# ==========================================================
# WELCOME SYSTEM
# ==========================================================

async def handle_welcome(client, chat_id: int, users: list, chat_title: str):
    status = await db.get_welcome_status(chat_id)
    if not status:
        return
    welcome_text = await db.get_welcome_message(chat_id) or DEFAULT_WELCOME
    for user in users:
        try:
            text = welcome_text.format(
                username=user.username or user.first_name,
                first_name=user.first_name,
                mention=user.mention,
                title=chat_title,
            )
        except Exception:
            text = DEFAULT_WELCOME.format(first_name=user.first_name, title=chat_title)
        try:
            await client.send_message(chat_id, text)
        except Exception as e:
            logger.error(f"🚨 Welcome error: {e}")

@Client.on_message(filters.new_chat_members & filters.group)
async def welcome_new_members(client, message: Message):
    await handle_welcome(client, message.chat.id, message.new_chat_members, message.chat.title)

@Client.on_message(filters.group & filters.command("welcome"))
async def welcome_toggle(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Admin only.")
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
        return await message.reply_text("⚙️ Usage: /welcome on/off")
    status = parts[1].lower() == "on"
    await db.set_welcome_status(message.chat.id, status)
    await message.reply_text("✅ Welcome ON." if status else "⚠️ Welcome OFF.")

# ==========================================================
# LOCK SYSTEM
# ==========================================================

@Client.on_message(filters.group & filters.command(["lock", "unlock"]))
async def lock_unlock_manager(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Admin only.")
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply_text("Usage: /lock <type>")
    
    lock_type = parts[1].lower()
    is_locking = message.command[0] == "lock"
    await db.set_lock(message.chat.id, lock_type, is_locking)
    await message.reply_text(f"{'🔒' if is_locking else '🔓'} {lock_type.capitalize()} updated.")

@Client.on_message(filters.group & ~filters.service, group=1)
async def enforce_locks(client, message: Message):
    if await is_power(client, message.chat.id, message.from_user.id):
        return
    locks = await db.get_locks(message.chat.id)
    if not locks: return

    # Simple logic check for URL/Sticker/Media
    if locks.get("url") and ("t.me" in str(message.text) or message.entities):
        await message.delete()
    elif locks.get("sticker") and message.sticker:
        await message.delete()
    elif locks.get("media") and (message.photo or message.video):
        await message.delete()

# ==========================================================
# MODERATION (Kick/Ban/Mute)
# ==========================================================

@Client.on_message(filters.group & filters.command("ban"))
async def ban_command(client, message):
    if not await is_power(client, message.chat.id, message.from_user.id): return
    user = await extract_target_user(client, message)
    if not user: return await message.reply_text("Who should I ban?")
    await client.ban_chat_member(message.chat.id, user.id)
    await message.reply_text(f"🚨 {user.mention} Banned.")

@Client.on_message(filters.group & filters.command("mute"))
async def mute_command(client, message):
    if not await is_power(client, message.chat.id, message.from_user.id): return
    user = await extract_target_user(client, message)
    if not user: return await message.reply_text("Who should I mute?")
    await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=False))
    await message.reply_text(f"🔇 {user.mention} Muted.")

@Client.on_message(filters.group & filters.command("promote"))
async def promote_command(client, message):
    if not await is_power(client, message.chat.id, message.from_user.id): return
    user = await extract_target_user(client, message)
    if not user: return
    await client.promote_chat_member(message.chat.id, user.id, ChatPrivileges(can_manage_chat=True, can_delete_messages=True))
    await message.reply_text(f"✅ {user.mention} is now Admin.")
