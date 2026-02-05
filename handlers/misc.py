# handlers/misc.py
from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards import start_menu_kb
from states import Flow
from aiogram.filters import Command
from data.emotions_data import EMOTIONS

def register_misc_handlers(dp, bot):
    # /help
    @dp.message(Command("help"))
    async def help_command(message: Message):
        await message.answer(
            "Я EmoJourney 🌱 — бот для отслеживания эмоций.\n\n"
            "Команды:\n"
            "/start — начать или вернуться в меню\n"
            "/help — показать это сообщение\n"
            "/stop — завершить текущий флоу\n\n"
            "Просто выбирай кнопки или пиши текст там, где разрешено."
        )

    # /stop
    @dp.message(Command("stop"))
    async def stop_command(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Флоу остановлен 💛\nТы вернулся в главное меню.",
            reply_markup=start_menu_kb()
        )
        await state.set_state(Flow.start_menu)

    # Дополнительно можно ловить "выход" через кнопки
    @dp.message(F.text == "🚪 Выйти")
    async def full_exit(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Береги себя 💛\nЕсли захочешь — просто напиши /start",
            reply_markup=ReplyKeyboardRemove()
        )

    @dp.message(Flow.start_menu)
    async def start_fallback(message: Message, state: FSMContext):
        await message.answer(
            "😅 Не понимаю тебя. Пожалуйста, используй кнопки или одну из команд:\n"
            "/start — начать или вернуться в меню\n"
            "/help — показать справку\n"
            "/stop — остановить текущий флоу",
            reply_markup=start_menu_kb()
        )

#    @dp.message()
#    async def global_fallback(message: Message):
#        # Можно добавить проверку, чтобы не повторять сообщение для start_menu
#        await message.answer(
#            "😅 Не понимаю тебя. Пожалуйста, выбирай кнопки или используй команды /start /help /stop"
#        )