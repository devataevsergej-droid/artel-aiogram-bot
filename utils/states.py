from aiogram.fsm.state import State, StatesGroup

class NameForm(StatesGroup):
    waiting_for_name = State()
