# handlers/start.py
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards import start_menu_kb, emotions_kb
from states import Flow
from data.emotions_data import EMOTIONS

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

    # Кнопка "Выйти"
    @dp.message(F.text == "🚪 Выйти")
    async def full_exit(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Береги себя 💛\nЕсли захочешь — просто напиши /start",
            reply_markup=None
        )

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
