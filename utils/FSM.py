from aiogram.fsm.state import StatesGroup, State


class SantaFSMGet(StatesGroup):
    GET_TEXT = State()
    GET_PHOTO = State()


class SantaFSMChange(StatesGroup):
    CHANGE_TEXT = State()
    CHANGE_PHOTO = State()
