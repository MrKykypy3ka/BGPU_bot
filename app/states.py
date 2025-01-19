from aiogram.fsm.state import StatesGroup, State


class Newsletter(StatesGroup):
    subscription = State()
    link = State()
    data = State()


class Admin(StatesGroup):
    login = State()