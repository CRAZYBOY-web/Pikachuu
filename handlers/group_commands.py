from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

@Client.on_message(filters.command(["lock", "unlock"]) & filters.group)
async def lock_system(client, message):
    # Admin check here...
    cmd = message.command[0]
    if len(message.command) < 2: return await message.reply_text("Use: /lock stickers")
    
    what = message.command[1]
    if cmd == "lock":
        if what == "stickers":
            await client.set_chat_permissions(message.chat.id, ChatPermissions(can_send_other_messages=False))
            await message.reply_text("🔒 **Stickers are now Locked!**")
    else:
        await client.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=True, can_send_other_messages=True))
        await message.reply_text("🔓 **Chat Unlocked!**")
