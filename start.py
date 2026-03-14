# ============================================================
# ༒ ᴘɪᴋᴀᴄʜᴜᴜ 亗 Start & Help System
# ============================================================
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID, BOT_NAME
import db  # Ensure you have your db.py set up for add_user and get_all_users

# --- START MENU FUNCTION ---
async def send_start_menu(message, user_name):
    text = f"""
✨ **Hello {user_name}!** ✨

👋 I am **{BOT_NAME}** 🤖 

**Highlights:**
─────────────────────────────
- 🛡️ Smart Anti-Spam & Link Shield
- 🔒 Adaptive Lock System (URLs, Media, etc.)
- ⚙️ Modular & Scalable Protection
- 📱 Sleek UI with Inline Controls

» More New Features coming soon ...
"""
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚒️ Add to Group ⚒️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("⌂ Support ⌂", url=SUPPORT_GROUP),
            InlineKeyboardButton("⌂ Update ⌂", url=UPDATE_CHANNEL),
        ],
        [
            InlineKeyboardButton("※ ŎŴɳēŔ ※", url=f"tg://user?id={OWNER_ID}"),
            InlineKeyboardButton("Repo", url="https://github.com/LearningBotsOfficial/Nomade"),
        ],
        [InlineKeyboardButton("📚 Help Commands 📚", callback_data="help")]
    ])

    if hasattr(message, 'click'): # Check if it's a callback query
        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await message.message.edit_media(media=media, reply_markup=buttons)
    else: # If it's a direct message
        await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)

# --- START COMMAND ---
@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    user = message.from_user
    await db.add_user(user.id, user.first_name)
    await send_start_menu(message, user.first_name)

# --- HELP MENU HANDLER ---
@Client.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query):
    text = """
╔══════════════════╗
      Help Menu
╚══════════════════╝

Choose a category below to explore commands:
─────────────────────────────
"""
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⌂ Greetings ⌂", callback_data="greetings"),
            InlineKeyboardButton("⌂ Locks ⌂", callback_data="locks"),
        ],
        [InlineKeyboardButton("⌂ Moderation ⌂", callback_data="moderation")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
    ])
    media = InputMediaPhoto(media=START_IMAGE, caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=buttons)
    await callback_query.answer()

# --- BACK TO START ---
@Client.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback(client, callback_query):
    await send_start_menu(callback_query, callback_query.from_user.first_name)
    await callback_query.answer()

# --- CATEGORY CALLBACKS (Greetings, Locks, Moderation) ---
@Client.on_callback_query(filters.regex(r"^(greetings|locks|moderation)$"))
async def categories_callback(client, callback_query):
    data = callback_query.data
    if data == "greetings":
        text = "╔══════════════════╗\n   ⚙ Welcome System\n╚══════════════════╝\n\n- /setwelcome <text>\n- /welcome on/off\n\nPlaceholders: {mention}, {first_name}, {id}"
    elif data == "locks":
        text = "╔══════════════════╗\n    ⚙ Locks System\n╚══════════════════╝\n\n- /lock <type>\n- /unlock <type>\n\nTypes: url, sticker, media, ads"
    else:
        text = "╔══════════════════╗\n  ⚙️ Moderation System\n╚══════════════════╝\n\n- /ban, /unban\n- /mute, /unmute\n- /warn, /promote"
    
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
    await callback_query.message.edit_media(media=InputMediaPhoto(START_IMAGE, caption=text), reply_markup=buttons)

# --- OWNER COMMANDS (Broadcast & Stats) ---
@Client.on_message(filters.private & filters.command("stats") & filters.user(OWNER_ID))
async def stats_command(client, message):
    users = await db.get_all_users()
    await message.reply_text(f"💡 **Total Bot Users:** {len(users)}")
