import motor.motor_asyncio
from config import Config

# --- MONGODB CONNECTION ---
client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URL)
db = client["Pikachuu_Bot_DB"]

# Collections
users_db = db.users
welcome_db = db.welcome
locks_db = db.locks
warns_db = db.warns

# ==========================================================
# 👤 USER MANAGEMENT & OWNER STATS
# ==========================================================

async def add_user(user_id, first_name):
    """Adds a user to the database or updates their name."""
    await users_db.update_one(
        {"user_id": user_id}, 
        {"$set": {"first_name": first_name}}, 
        upsert=True
    )

async def get_all_users():
    """Returns a list of all unique user IDs for broadcasting."""
    return [user["user_id"] async for user in users_db.find()]

async def get_stats():
    """Returns the total number of users in the database."""
    return await users_db.count_documents({})

# ==========================================================
# 👋 WELCOME SYSTEM
# ==========================================================

async def set_welcome_status(chat_id, status: bool):
    """Enables or disables welcome messages for a chat."""
    await welcome_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"status": status}},
        upsert=True
    )

async def get_welcome_status(chat_id):
    """Checks if welcome is ON (True) or OFF (False)."""
    res = await welcome_db.find_one({"chat_id": chat_id})
    return res.get("status", True) if res else True

async def set_welcome_message(chat_id, text):
    """Saves a custom welcome text for the group."""
    await welcome_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"message": text}},
        upsert=True
    )

async def get_welcome_message(chat_id):
    """Retrieves the custom welcome text."""
    res = await welcome_db.find_one({"chat_id": chat_id})
    return res.get("message") if res else None

# ==========================================================
# 🔒 LOCK SYSTEM
# ==========================================================

async def set_lock(chat_id, lock_type, status: bool):
    """Locks or unlocks a specific type (e.g., 'url', 'sticker')."""
    await locks_db.update_one(
        {"chat_id": chat_id},
        {"$set": {f"locks.{lock_type}": status}},
        upsert=True
    )

async def get_locks(chat_id):
    """Returns a dictionary of all active locks for a chat."""
    res = await locks_db.find_one({"chat_id": chat_id})
    return res.get("locks", {}) if res else {}

# ==========================================================
# ⚠️ WARNING SYSTEM
# ==========================================================

async def add_warn(chat_id, user_id):
    """Increments warn count and returns the new total."""
    res = await warns_db.find_one_and_update(
        {"chat_id": chat_id, "user_id": user_id},
        {"$inc": {"count": 1}},
        upsert=True,
        return_document=motor.motor_asyncio.ReturnDocument.AFTER
    )
    return res.get("count", 0)

async def get_warns(chat_id, user_id):
    """Checks current warning count for a user."""
    res = await warns_db.find_one({"chat_id": chat_id, "user_id": user_id})
    return res.get("count", 0) if res else 0

async def reset_warns(chat_id, user_id):
    """Removes all warnings for a user in a specific chat."""
    await warns_db.delete_one({"chat_id": chat_id, "user_id": user_id})
