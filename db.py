import motor.motor_asyncio
from config import Config

# Initialize MongoDB Client
# It uses the MONGO_URI from your config.py
client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URL)
db = client["Pikachuu_Bot_DB"]

# Collections
users_db = db.users
chats_db = db.chats
welcome_db = db.welcome

# --- USER FUNCTIONS ---

async def add_user(user_id, first_name):
    """Adds a new user to the database if they don't exist."""
    user = await users_db.find_one({"user_id": user_id})
    if not user:
        await users_db.insert_one({"user_id": user_id, "first_name": first_name})
        return True
    return False

async def get_all_users():
    """Returns a list of all user IDs for broadcasting."""
    users = []
    async for user in users_db.find():
        users.append(user["user_id"])
    return users

# --- WELCOME SYSTEM FUNCTIONS ---

async def set_welcome(chat_id, welcome_text):
    """Saves a custom welcome message for a specific group."""
    await welcome_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"text": welcome_text}},
        upsert=True
    )

async def get_welcome(chat_id):
    """Retrieves the custom welcome message for a group."""
    result = await welcome_db.find_one({"chat_id": chat_id})
    return result["text"] if result else None

# --- STATS FUNCTIONS ---

async def get_stats():
    """Returns the total count of users and groups."""
    user_count = await users_db.count_documents({})
    return user_count
