from aiogram.fsm.state import StatesGroup, State


class Question(StatesGroup):
    text = State()
    user = State()


class Admin(StatesGroup):
    login = State()

class Answer(StatesGroup):
    user = State()
    text = State()