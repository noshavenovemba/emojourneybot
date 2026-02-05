import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS emotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            emotion TEXT,
            comment TEXT,
            task_result TEXT,
            photo_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        await db.commit()

async def save_to_db(data: dict):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO emotions (user_id, emotion, comment, task_result, photo_id)
        VALUES (?, ?, ?, ?, ?)
        """, (
            data["user_id"],
            data["emotion"],
            data.get("comment"),
            data.get("task_result"),
            data.get("photo_id")
        ))
        await db.commit()