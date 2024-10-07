from aiogram.fsm.state import StatesGroup, State


class SetPercentState(StatesGroup):
    min_percent = State()
    max_percent = State()
    channel_name_add = State()
    channel_name_remove = State()