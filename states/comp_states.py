from aiogram.dispatcher.filters.state import StatesGroup, State


class CompStates(StatesGroup):
    name = State()
    number = State()
    location = State()
    comp = State()
    processor = State()
    memory = State()
    ram = State()
    price = State()
    confirm = State()
