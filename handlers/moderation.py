from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.enums import ChatMemberStatus
import logging

# Logic to check if the person using the command is an admin
async def is_admin(client, chat_id, user_id):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

# 🚨 BAN COMMAND
@Client.on_message(filters.group & filters.command("ban"))
async def ban_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.")
    
    # Check if replying to a user
    if not message.reply_to_message:
        return await message.reply_text("⚠️ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ʙᴀɴ ᴛʜᴇᴍ.")

    user_id = message.reply_to_message.from_user.id
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"🚨 {message.reply_to_message.from_user.mention} ʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ.")
    except Exception as e:
        await message.reply_text(f"❌ ᴇʀʀᴏʀ: {e}")

# 🔇 MUTE COMMAND
@Client.on_message(filters.group & filters.command("mute"))
async def mute_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return
    
    if not message.reply_to_message:
        return await message.reply_text("⚠️ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴍᴜᴛᴇ ᴛʜᴇᴍ.")

    user_id = message.reply_to_message.from_user.id
    try:
        await client.restrict_chat_member(
            message.chat.id, 
            user_id, 
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.reply_text(f"🔇 {message.reply_to_message.from_user.mention} ᴍᴜᴛᴇᴅ.")
    except Exception as e:
        await message.reply_text(f"❌ ᴇʀʀᴏʀ: {e}")

# 👢 KICK COMMAND
@Client.on_message(filters.group & filters.command("kick"))
async def kick_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return
    
    if not message.reply_to_message:
        return await message.reply_text("⚠️ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴋɪᴄᴋ ᴛʜᴇᴍ.")

    user_id = message.reply_to_message.from_user.id
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await client.unban_chat_member(message.chat.id, user_id) # Unban immediately so they can rejoin
        await message.reply_text(f"👢 {message.reply_to_message.from_user.mention} ᴋɪᴄᴋᴇᴅ.")
    except Exception as e:
        await message.reply_text(f"❌ ᴇʀʀᴏʀ: {e}")
