from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.emotions_data import EMOTIONS 

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

def continue_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="😊 Да, выбрать эмоцию")],
            [KeyboardButton(text="🚪 Нет, закончить")]
        ],
        resize_keyboard=True
    )

def start_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Начать"), KeyboardButton(text="🌱 О боте")],
#           [KeyboardButton(text="⚙️ Профиль / Настройки"), KeyboardButton(text="📚 Мои тьюториалы")],
            [KeyboardButton(text="📈 Динамика эмоций"), KeyboardButton(text="💡 Советы и практики")],
            [KeyboardButton(text="🚪 Выйти")]
        ],
        resize_keyboard=True
    )