from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, ChatPrivileges, ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
import db
import logging

# --- sᴇᴛᴛɪɴɢs ---
DEFAULT_WELCOME = "👋 ᴡᴇʟᴄᴏᴍᴇ {mention} ᴛᴏ {title}!"
logger = logging.getLogger(__name__)

# --- ᴀᴅᴍɪɴ ᴄʜᴇᴄᴋ ʜᴇʟᴘᴇʀ ---
async def is_power(client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception:
        return False

# --- ᴜsᴇʀ ᴇxᴛʀᴀᴄᴛᴏʀ ʜᴇʟᴘᴇʀ ---
async def extract_target_user(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return None
    arg = parts[1]
    try:
        return await client.get_users(arg)
    except Exception:
        return None

# ==========================================================
# ᴡᴇʟᴄᴏᴍᴇ sʏsᴛᴇᴍ
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
            await client.send_message(chat_id, text)
        except Exception as e:
            logger.error(f"🚨 ᴡᴇʟᴄᴏᴍᴇ ᴇʀʀᴏʀ: {e}")

@Client.on_message(filters.new_chat_members)
async def on_new_member(client, message: Message):
    await handle_welcome(client, message.chat.id, message.new_chat_members, message.chat.title)

@Client.on_message(filters.group & filters.command("welcome"))
async def welcome_toggle(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs.**")
    parts = message.text.split()
    if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
        return await message.reply_text("⚙️ **ᴜsᴀɢᴇ:** `/welcome on` ᴏʀ `/welcome off`")
    status = parts[1].lower() == "on"
    await db.set_welcome_status(message.chat.id, status)
    await message.reply_text(f"{'✅' if status else '⚠️'} **ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs:** `{'ᴏɴ' if status else 'ᴏꜰꜰ'}`")

@Client.on_message(filters.group & filters.command("setwelcome"))
async def set_welcome(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ **ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ʀᴇǫᴜɪʀᴇᴅ.**")
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply_text("📝 **ᴜsᴀɢᴇ:** `/setwelcome <ᴍᴇssᴀɢᴇ>`\n\n**ᴛᴀɢs:** `{mention}`, `{first_name}`, `{title}`")
    await db.set_welcome_message(message.chat.id, parts[1])
    await message.reply_text("✅ **ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ sᴀᴠᴇᴅ!**")

# ==========================================================
# ʟᴏᴄᴋ sʏsᴛᴇᴍ
# ==========================================================

@Client.on_message(filters.group & filters.command(["lock", "unlock"]))
async def lock_unlock_handler(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ **ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ʀᴇǫᴜɪʀᴇᴅ.**")
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply_text("⚙️ **ᴜsᴀɢᴇ:** `/lock <type>`\n**ᴛʏᴘᴇs:** `url`, `sticker`, `media`, `username`, `forward`")
    
    lock_type = parts[1].lower()
    is_lock = message.command[0].lower() == "lock"
    
    if lock_type not in ["url", "sticker", "media", "username", "forward"]:
        return await message.reply_text("⚠️ **ɪɴᴠᴀʟɪᴅ ʟᴏᴄᴋ ᴛʏᴘᴇ.**")
        
    await db.set_lock(message.chat.id, lock_type, is_lock)
    await message.reply_text(f"{'🔒' if is_lock else '🔓'} **{lock_type.upper()}** {'ʟᴏᴄᴋᴇᴅ' if is_lock else 'ᴜɴʟᴏᴄᴋᴇᴅ'} **sᴜᴄᴄᴇssꜰᴜʟʟʏ!**")

@Client.on_message(filters.group & ~filters.service, group=1)
async def lock_enforcer(client, message: Message):
    if not message.from_user or await is_power(client, message.chat.id, message.from_user.id):
        return
    locks = await db.get_locks(message.chat.id)
    if not locks: return

    # URL Check
    if locks.get("url") and (message.entities or message.caption_entities):
        for ent in (message.entities or message.caption_entities):
            if ent.type in ["url", "text_link"]:
                return await message.delete()
    
    # Other Checks
    if locks.get("sticker") and message.sticker: await message.delete()
    elif locks.get("media") and (message.photo or message.video or message.document): await message.delete()
    elif locks.get("username") and message.text and "@" in message.text: await message.delete()
    elif locks.get("forward") and message.forward_date: await message.delete()

# ==========================================================
# ᴍᴏᴅᴇʀᴀᴛɪᴏɴ sʏsᴛᴇᴍ
# ==========================================================

@Client.on_message(filters.group & filters.command(["ban", "unban", "mute", "unmute", "kick"]))
async def moderation_handler(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id):
        return
    user = await extract_target_user(client, message)
    if not user:
        return await message.reply_text("⚠️ **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴘʀᴏᴠɪᴅᴇ @ᴜsᴇʀɴᴀᴍᴇ.**")

    cmd = message.command[0].lower()
    try:
        if cmd == "ban":
            await client.ban_chat_member(message.chat.id, user.id)
            await message.reply_text(f"🚨 {user.mention} **ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ.**")
        elif cmd == "unban":
            await client.unban_chat_member(message.chat.id, user.id)
            await message.reply_text(f"✅ {user.mention} **ᴜɴʙᴀɴɴᴇᴅ.**")
        elif cmd == "mute":
            await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=False))
            await message.reply_text(f"🔇 {user.mention} **ᴍᴜᴛᴇᴅ.**")
        elif cmd == "unmute":
            await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            await message.reply_text(f"🔊 {user.mention} **ᴜɴᴍᴜᴛᴇᴅ.**")
        elif cmd == "kick":
            await client.ban_chat_member(message.chat.id, user.id)
            await client.unban_chat_member(message.chat.id, user.id)
            await message.reply_text(f"👢 {user.mention} **ᴋɪᴄᴋᴇᴅ.**")
    except Exception as e:
        await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** `{e}`")

# ==========================================================
# ᴡᴀʀɴ sʏsᴛᴇᴍ
# ==========================================================

@Client.on_message(filters.group & filters.command("warn"))
async def warn_user(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id): return
    user = await extract_target_user(client, message)
    if not user: return
    
    warns = await db.add_warn(message.chat.id, user.id)
    if warns >= 3:
        await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=False))
        await db.reset_warns(message.chat.id, user.id)
        await message.reply_text(f"🚫 {user.mention} **ᴍᴜᴛᴇᴅ ꜰᴏʀ ʀᴇᴀᴄʜɪɴɢ ᴍᴀx ᴡᴀʀɴs (3/3).**")
    else:
        await message.reply_text(f"⚠️ {user.mention} **ʜᴀs ʙᴇᴇɴ ᴡᴀʀɴᴇᴅ! ({warns}/3)**")

@Client.on_message(filters.group & filters.command("resetwarns"))
async def reset_warns_cmd(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id): return
    user = await extract_target_user(client, message)
    if not user: return
    await db.reset_warns(message.chat.id, user.id)
    await message.reply_text(f"✅ **ᴡᴀʀɴs ʀᴇsᴇᴛ ꜰᴏʀ** {user.mention}.")

# ==========================================================
# ᴘʀᴏᴍᴏᴛᴇ / ᴅᴇᴍᴏᴛᴇ
# ==========================================================

@Client.on_message(filters.group & filters.command("promote"))
async def promote_cmd(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id): return
    user = await extract_target_user(client, message)
    if not user: return
    try:
        await client.promote_chat_member(message.chat.id, user.id, ChatPrivileges(can_manage_chat=True, can_delete_messages=True, can_restrict_members=True, can_invite_users=True, can_pin_messages=True))
        await message.reply_text(f"✅ {user.mention} **ɪs ɴᴏᴡ ᴀɴ ᴀᴅᴍɪɴ!**")
    except Exception as e:
        await message.reply_text(f"❌ **ꜰᴀɪʟᴇᴅ:** `{e}`")

@Client.on_message(filters.group & filters.command("demote"))
async def demote_cmd(client, message: Message):
    if not await is_power(client, message.chat.id, message.from_user.id): return
    user = await extract_target_user(client, message)
    if not user: return
    try:
        await client.promote_chat_member(message.chat.id, user.id, ChatPrivileges(can_manage_chat=False))
        await message.reply_text(f"✅ {user.mention} **ᴅᴇᴍᴏᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ.**")
    except Exception as e:
        await message.reply_text(f"❌ **ꜰᴀɪʟᴇᴅ:** `{e}`")
