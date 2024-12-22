from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start_city = State()
    end_city = State()
    forecast_days = State()
