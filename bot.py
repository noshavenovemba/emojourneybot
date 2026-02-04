import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# =========================
# CONFIG — EDIT THIS
# =========================
BOT_TOKEN = "8581408814:AAH7tKWRf2HxaY1XcjMWg69gl6eDnOSAapw"
TUTOR_CHAT_ID = 160355067

DB_NAME = "emojourney.db"

# =========================
# EMOTIONS DATA
# =========================
EMOTIONS = {
    "😢 Грусть": {
        "advice": "Тяжело… Попробуй записать, что вызывает грусть.",
        "task": (
            "1. Что вызывает грусть?\n"
            "2. События → мысли → ощущения\n"
            "3. Что может немного помочь?"
        )
    },
    "😍 Радость": {
        "advice": "Супер! Заметь, что именно тебя радует сегодня.",
        "task": (
            "1. Что вызвало радость?\n"
            "2. Где ощущается в теле?\n"
            "3. Как можно усилить это чувство?"
        )
    },
    "😡 Злость": {
        "advice": "Чувство гнева важно замечать.",
        "task": (
            "1. Что вызвало злость?\n"
            "2. Где ощущается в теле?\n"
            "3. Что помогло отпустить напряжение?"
        )
    },
    "😨 Страх": {
        "advice": "Страх — нормальная реакция.",
        "task": (
            "1. Что вызывает страх?\n"
            "2. Что помогает чувствовать себя безопаснее?\n"
            "3. Одна стратегия преодоления."
        )
    }
}

# =========================
# STATES
# =========================
class Flow(StatesGroup):
    choosing_emotion = State()
    writing_comment = State()
    doing_task = State()
    sending_to_tutor = State()

# =========================
# KEYBOARDS
# =========================
def emotions_kb():
    buttons = [KeyboardButton(text=e) for e in EMOTIONS.keys()]
    return ReplyKeyboardMarkup(
        keyboard=[buttons[i:i+2] for i in range(0, len(buttons), 2)],
        resize_keyboard=True
    )

def next_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="➡️ Следующее: задание")]],
        resize_keyboard=True
    )

def send_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📤 Отправить тьютору")]],
        resize_keyboard=True
    )

# =========================
# DATABASE
# =========================
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

# =========================
# BOT SETUP
# =========================
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# =========================
# HANDLERS
# =========================
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Привет! Добро пожаловать в EmoJourney 🌱\n\n"
        "Выбери эмоцию, которая лучше всего описывает твоё состояние:",
        reply_markup=emotions_kb()
    )
    await state.set_state(Flow.choosing_emotion)

@dp.message(Flow.choosing_emotion)
async def choose_emotion(message: Message, state: FSMContext):
    if message.text not in EMOTIONS:
        await message.answer("Пожалуйста, выбери эмоцию кнопкой 👇")
        return

    await state.update_data(emotion=message.text)
    await message.answer("Опиши, что вызвало эту эмоцию:")
    await state.set_state(Flow.writing_comment)

@dp.message(Flow.writing_comment)
async def comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    emotion_data = EMOTIONS[data["emotion"]]

    await message.answer(
        f"{emotion_data['advice']}\n\n"
        f"Задание:\n{emotion_data['task']}",
        reply_markup=next_kb()
    )
    await state.set_state(Flow.doing_task)

@dp.message(Flow.doing_task)
async def next_step_auto(message: Message, state: FSMContext):
    # Automatically treat user message as task result
    await state.update_data(task_result=message.text)
    await message.answer("Спасибо 💛 Я передал это тьютору.", reply_markup=emotions_kb())
    await state.set_state(Flow.choosing_emotion)

    await message.answer("Хотите выбрать другую эмоцию или что-то еще обсудить? 🌱")

    data = await state.get_data()
    photo_id = message.photo[-1].file_id if message.photo else None

    # Send to tutor
    await bot.send_message(
        TUTOR_CHAT_ID,
        f"🧠 EmoJourney\n"
        f"User ID: {message.from_user.id}\n"
        f"Эмоция: {data['emotion']}\n"
        f"Комментарий: {data['comment']}\n"
        f"Результат:\n{data['task_result'] or '—'}"
    )
    if photo_id:
        await bot.send_photo(TUTOR_CHAT_ID, photo_id)

    # Reset to choosing emotion
    await state.set_state(Flow.choosing_emotion)


@dp.message(Flow.sending_to_tutor)
async def send_to_tutor(message: Message, state: FSMContext):
    data = await state.get_data()

    photo_id = None
    text = message.text or message.caption

    if message.photo:
        photo_id = message.photo[-1].file_id

    await save_to_db({
        "user_id": message.from_user.id,
        "emotion": data["emotion"],
        "comment": data["comment"],
        "task_result": text,
        "photo_id": photo_id
    })

    # Send to tutor
    await bot.send_message(
        TUTOR_CHAT_ID,
        f"🧠 EmoJourney\n"
        f"User ID: {message.from_user.id}\n"
        f"Эмоция: {data['emotion']}\n"
        f"Комментарий: {data['comment']}\n"
        f"Результат:\n{text or '—'}"
    )

    if photo_id:
        await bot.send_photo(TUTOR_CHAT_ID, photo_id)

    await message.answer(
        "Спасибо 💛 Я передал это тьютору.",
        reply_markup=emotions_kb()
    )
    await state.set_state(Flow.choosing_emotion)

# =========================
# MAIN
# =========================
async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
