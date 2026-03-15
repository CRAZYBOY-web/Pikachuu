import motor.motor_asyncio
from config import MONGO_URI, DB_NAME
import logging

# sᴇᴛᴜᴘ ʟᴏɢɢɪɴɢ
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    logging.info("✅ ᴍᴏɴɢᴏᴅʙ ᴄᴏɴɴᴇᴄᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!")
except Exception as e:
    logging.error(f"❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴍᴏɴɢᴏᴅʙ: {e}")

# ==========================================================
# 👋 ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ sʏsᴛᴇᴍ
# ==========================================================

async def set_welcome_message(chat_id, text: str):
    await db.welcome.update_one(
        {"chat_id": chat_id},
        {"$set": {"message": text}},
        upsert=True
    )

async def get_welcome_message(chat_id):
    data = await db.welcome.find_one({"chat_id": chat_id})
    return data.get("message") if data else None

async def set_welcome_status(chat_id, status: bool):
    await db.welcome.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

async def get_welcome_status(chat_id) -> bool:
    data = await db.welcome.find_one({"chat_id": chat_id})
    if not data:  # Default is ON
        return True
    return bool(data.get("enabled", True))

# ==========================================================
# 🔒 ʟᴏᴄᴋ sʏsᴛᴇᴍ
# ==========================================================

async def set_lock(chat_id, lock_type, status: bool):
    await db.locks.update_one(
        {"chat_id": chat_id},
        {"$set": {f"locks.{lock_type}": status}},
        upsert=True
    )

async def get_locks(chat_id):
    data = await db.locks.find_one({"chat_id": chat_id})
    return data.get("locks", {}) if data else {}

# ==========================================================
# ⚠️ ᴡᴀʀɴ sʏsᴛᴇᴍ
# ==========================================================

async def add_warn(chat_id: int, user_id: int) -> int:
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    warns = data.get("count", 0) + 1 if data else 1

    await db.warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": warns}},
        upsert=True
    )
    return warns

async def get_warns(chat_id: int, user_id: int) -> int:
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    return data.get("count", 0) if data else 0

async def reset_warns(chat_id: int, user_id: int):
    await db.warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": 0}},
        upsert=True
    )

# ==========================================================
# 👤 ᴜsᴇʀ sʏsᴛᴇᴍ & sᴛᴀᴛs
# ==========================================================

async def add_user(user_id, first_name):
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"first_name": first_name}},
        upsert=True
    )

async def get_all_users():
    cursor = db.users.find({}, {"_id": 0, "user_id": 1})
    users = []
    async for document in cursor:
        if "user_id" in document:
            users.append(document["user_id"])
    return users

async def get_stats():
    """Returns total user count for the /stats command"""
    return await db.users.count_documents({})

# ==========================================================
# 🧹 ᴄʟᴇᴀɴᴜᴘ ᴜᴛɪʟs
# ==========================================================

async def clear_group_data(chat_id: int):
    await db.welcome.delete_one({"chat_id": chat_id})
    await db.locks.delete_one({"chat_id": chat_id})
    await db.warns.delete_many({"chat_id": chat_id})
