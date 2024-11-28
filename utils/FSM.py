from aiogram.fsm.state import StatesGroup, State


class FSM_get(StatesGroup):
    GET_TEXT = State()
    GET_PHOTO = State()


class FSM_change(StatesGroup):
    CHANGE_TEXT = State()
    CHANGE_PHOTO = State()
