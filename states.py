from aiogram.fsm.state import StatesGroup, State

class Flow(StatesGroup):
    start_menu = State()
    choosing_emotion = State()
    writing_comment = State()
    doing_task = State()
    sending_to_tutor = State()
    after_task = State()
