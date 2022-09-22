from aiogram.dispatcher.filters.state import StatesGroup, State

class Test(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()

class Lang(StatesGroup):
    step1 = State()
    step2 = State()