from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .handler import RouterSanta
from aiogram.types import CallbackQuery
from utils.FSM import FSM_get

async def recipient(call:CallbackQuery):
    await call.answer()
    
    if call.from_user.id != call.message.chat.id:
        await call.message.answer(text='Пиши в лс дуралей')
        return

async def mywish(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Напишите ваши пожелания')

    await state.set_state(FSM_get.GET_TEXT)


async def recipientwish()



async def FSM_santa(message: Message, state: FSMContext):
    await state.update_data(wish=message.text)
    await message.answer('Номер договора')
    await state.set_state(FSM_get.GET_TEXT)


async def FSM_sants_wish(message: Message, state: FSMContext):
    


async def check(chat_id, user_id):
    '''
    
    '''
    if chat_id == user_id:
        return