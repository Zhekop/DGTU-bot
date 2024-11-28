from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .handler import RouterSanta
from aiogram.types import CallbackQuery

async def recipient(call:CallbackQuery):
    await call.answer()
    
    if call.from_user.id != call.message.chat.id:
        await call.message.answer(text='Пиши в лс дуралей')
        return

async def mywish(call: CallbackQuery):
    await call.answer()
    await call.message.answer('Напишите ваши пожелания')



async def recipientwish()



async def FSM_santa(state:FSMContext):
    state


async def check(chat_id, user_id):
    '''
    
    '''
    if chat_id == user_id:
        return