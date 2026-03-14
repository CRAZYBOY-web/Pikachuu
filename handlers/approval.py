from pyrogram import Client, filters

@Client.on_chat_join_request()
async def approve_requests(client, request):
    # Logic to approve users instantly
    await client.approve_chat_join_request(request.chat.id, request.from_user.id)
