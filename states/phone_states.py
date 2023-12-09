from aiogram.dispatcher.filters.state import StatesGroup, State


class PhoneStates(StatesGroup):
    name = State()
    number = State()
    location = State()
    phone = State()
    memory = State()
    ram = State()
    price = State()
    confirm = State()


