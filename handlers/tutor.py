# handlers/tutor.py
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import Flow
from db import save_to_db
from keyboards import emotions_kb
from config import TUTOR_CHAT_ID
from data.emotions_data import EMOTIONS

def register_tutor_handlers(dp, bot):
    @dp.message(Flow.sending_to_tutor)
    async def send_to_tutor(message: Message, state: FSMContext):
        data = await state.get_data()
        text = message.text or message.caption
        photo_id = message.photo[-1].file_id if message.photo else None

        # Сохраняем в базу
        await save_to_db({
            "user_id": message.from_user.id,
            "emotion": data["emotion"],
            "comment": data["comment"],
            "task_result": text,
            "photo_id": photo_id
        })

        # Отправляем тьютору
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

        # Сообщение пользователю
        await message.answer(
            "Спасибо 💛 Я передал это тьютору.",
            reply_markup=emotions_kb()
        )
        await state.set_state(Flow.choosing_emotion)
