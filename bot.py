import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db import init_db

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

from handlers import start, emotions, after_task, tutor, misc

# регистрируем хэндлеры
start.register_start_handlers(dp, bot)
emotions.register_emotions_handlers(dp, bot)
after_task.register_after_task_handlers(dp, bot)
tutor.register_tutor_handlers(dp, bot)
misc.register_misc_handlers(dp, bot)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
