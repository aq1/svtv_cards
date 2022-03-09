from aiogram.dispatcher.filters.state import StatesGroup, State

class State_SVTV(StatesGroup):
    name_pattern = State()
    name_word = State()
    name_minusword = State()
    add_channel = State()
    remove_channel = State()