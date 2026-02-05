# handlers/after_task.py
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import Flow
from keyboards import emotions_kb, continue_kb, start_menu_kb
from data.emotions_data import EMOTIONS

def register_after_task_handlers(dp, bot):  # <- добавили bot как аргумент
    @dp.message(Flow.after_task, F.text == "😊 Да, выбрать эмоцию")
    async def after_task_continue(message: Message, state: FSMContext):
        await message.answer(
            "Хорошо 🌱 Выбери эмоцию:",
            reply_markup=emotions_kb()
        )
        await state.set_state(Flow.choosing_emotion)


    @dp.message(Flow.after_task, F.text == "🚪 Нет, закончить")
    async def after_task_quit(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Хорошо 💛 Я здесь, если понадобится.\n\nЧто хочешь сделать дальше?",
            reply_markup=start_menu_kb()
        )

    @dp.message(Flow.after_task)
    async def after_task_wrong_input(message: Message):
        await message.answer(
            "Пожалуйста, выбери вариант кнопкой 👇",
            reply_markup=continue_kb()
        )
