from pyrogram import Client, filters
from config import Config
import db # For saving custom welcome text

@Client.on_chat_join_request()
async def auto_approve(client, request):
    await client.approve_chat_join_request(request.chat.id, request.from_user.id)
    try:
        await client.send_message(request.from_user.id, f"⚡ **Approved! Welcome to {request.chat.title}**")
    except:
        pass

@Client.on_message(filters.new_chat_members)
async def welcome_msg(client, message):
    chat_id = message.chat.id
    # Get custom welcome from DB or use default
    custom_data = await db.get_welcome(chat_id)
    text = custom_data if custom_data else "Welcome {mention} to {title}! ⚡"
    
    for member in message.new_chat_members:
        final_text = text.format(
            first_name=member.first_name,
            mention=member.mention,
            id=member.id,
            title=message.chat.title
        )
        await message.reply_text(final_text)
