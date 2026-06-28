# handlers/start.py
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards import start_menu_kb, emotions_kb
from states import Flow
from data.emotions_data import EMOTIONS
import aiosqlite
from config import DB_NAME

def register_start_handlers(dp, bot):
    # Стартовое меню — кнопка "Начать"
    @dp.message(F.text == "▶️ Начать")
    async def restart_flow(message: Message, state: FSMContext):
        await message.answer(
            "Давай начнём 🌱\nВыбери эмоцию:",
            reply_markup=emotions_kb()
        )
        await state.set_state(Flow.choosing_emotion)

    # Кнопка "О боте"
    @dp.message(F.text == "🌱 О боте")
    async def about_bot(message: Message):
        await message.answer(
            "EmoJourney — безопасное пространство для отслеживания эмоций 💛\n\n"
            "Ты можешь возвращаться в любой момент, чтобы заметить своё состояние и прожить его мягко.",
            reply_markup=start_menu_kb()
        )

    @dp.message(F.text == "💡 Советы и практики")
    async def about_bot(message: Message):
        await message.answer(
            "Здесь будут практики",
            reply_markup=start_menu_kb()
        )

    # Кнопка "Выйти"
    @dp.message(F.text == "🚪 Выйти")
    async def full_exit(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Береги себя 💛\nЕсли захочешь — просто напиши /start",
            reply_markup=None
        )
    @dp.message(F.text == "⚙️ Профиль / Настройки")
    async def profile_settings(message: Message, state: FSMContext):
        # Получаем имя пользователя и язык Telegram
        user_name = message.from_user.first_name or "Пользователь"
        user_username = f"@{message.from_user.username}" if message.from_user.username else "—"
        user_id = message.from_user.id
        user_language = message.from_user.language_code or "не указан"
        
        # Можно, если есть в state, добавить возраст или другие данные
        data = await state.get_data()
        user_age = data.get("age", "не указан")  # если хранили ранее
        
        # Отправляем информацию
        await message.answer(
            f"⚙️ Профиль / Настройки\n\n"
            f"Имя: {user_name}\n"
            f"Никнейм: {user_username}\n"
            f"ID: {user_id}\n"
            f"Возраст: {user_age}\n"
            f"Язык Telegram: {user_language}\n\n"
            "Здесь ты можешь обновить свои данные (в будущем можно добавить кнопки для редактирования).",
            reply_markup=None  # клавиатура убрана
        )

    @dp.message(F.text == "📈 Динамика эмоций")
    async def show_emotion_history(message: Message, state: FSMContext):
        user_id = message.from_user.id
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT emotion, comment, created_at FROM emotions "
                "WHERE user_id = ? ORDER BY created_at DESC LIMIT 10",
                (user_id,)
            )
            rows = await cursor.fetchall()

        if not rows:
            await message.answer("📊 Пока нет записей о твоих эмоциях.")
            return

        response = "📈 Последние 10 твоих эмоций:\n\n"
        for i, (emotion, comment, created_at) in enumerate(rows[::-1], start=1):
            date_str = str(created_at).split(' ')[0] if created_at else "—"
            response += f"{i}. {emotion} — {date_str}\n   {comment or '—'}\n"

        await message.answer(response)   

    # Также обработка /start
    from aiogram.filters import Command
    @dp.message(Command("start"))
    async def start_command(message: Message, state: FSMContext):
        username = message.from_user.first_name or "друг"
        await state.clear()
        await message.answer(
            f"Привет, {username}! 👋\n"
            "Я EmoJourney 🌱\n\n"
            "Что ты хочешь сделать?",
            reply_markup=start_menu_kb()  # клавиатура с кнопками "Начать", "О боте", "Выйти"
        )
        await state.set_state(Flow.start_menu)
