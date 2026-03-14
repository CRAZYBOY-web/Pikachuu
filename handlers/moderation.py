from pyrogram import Client, filters, enums
from pyrogram.types import ChatPrivileges

@Client.on_message(filters.command(["ban", "mute", "kick", "promote"]) & filters.group)
async def admin_cmds(client, message):
    # Check if sender is admin
    self = await client.get_chat_member(message.chat.id, message.from_user.id)
    if self.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return

    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to take action!")

    user_id = message.reply_to_message.from_user.id
    cmd = message.command[0]

    if cmd == "ban":
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text("⚡ **User Electrified and Banned!**")
    elif cmd == "mute":
        await client.restrict_chat_member(message.chat.id, user_id, ChatPrivileges(can_send_messages=False))
        await message.reply_text("🔇 **User Silenced!**")
    elif cmd == "promote":
        await client.promote_chat_member(message.chat.id, user_id, ChatPrivileges(can_manage_chat=True, can_delete_messages=True, can_restrict_members=True))
        await message.reply_text("💎 **User Promoted to Admin!**")
