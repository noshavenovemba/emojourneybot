# handlers/emotions.py
from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import Flow
from keyboards import emotions_kb, next_kb, continue_kb
from config import EMOTIONS, TUTOR_CHAT_ID
from db import save_to_db
from data.emotions_data import EMOTIONS

def register_emotions_handlers(dp, bot):
    @dp.message(Flow.choosing_emotion)
    async def choose_emotion(message: Message, state: FSMContext):
        if message.text not in EMOTIONS:
            await message.answer(
                "Пожалуйста, выбери эмоцию кнопкой 👇",
                reply_markup=emotions_kb()
            )
            return

        await state.update_data(emotion=message.text)
        await message.answer(
            "Опиши, что вызвало эту эмоцию:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Flow.writing_comment)

    @dp.message(Flow.writing_comment)
    async def comment(message: Message, state: FSMContext):
        await state.update_data(comment=message.text)
        data = await state.get_data()
        emotion_data = EMOTIONS[data["emotion"]]

        await message.answer(
            f"{emotion_data['advice']}\n\nЗадание:\n{emotion_data['task']}",
            reply_markup=next_kb()
        )
        await state.set_state(Flow.doing_task)

    @dp.message(Flow.doing_task)
    async def receive_task_result(message: Message, state: FSMContext):
        text = message.text or message.caption
        photo_id = message.photo[-1].file_id if message.photo else None

        await state.update_data(task_result=text, photo_id=photo_id)

        await message.answer(
            "Спасибо 💛 Я передал это тьютору.\n\n"
            "Хотите выбрать другую эмоцию или что-то еще обсудить? 🌱",
            reply_markup=continue_kb()
        )

        await state.set_state(Flow.after_task)
