from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from utils import Database, SantaRepo
from utils.FSM import SantaFSMGet, SantaFSMChange

from .wishes import recipient, mywish, recipientwish, FSM_santa, update, change, check

RouterSanta = Router()


@RouterSanta.message(Command('santa'))
async def getSantaMenu(message:Message):
    
    name = f'{message.from_user.full_name}'
    if text:=check(chat_id=message.chat.id, user_id=message.from_user.id, name=name):
        await message.answer(text=text)
        return
    
    inline_keyboard = [
        [InlineKeyboardButton(text='Получатель', callback_data='santa_get_recipient')],
        [InlineKeyboardButton(text='Мои пожелания', callback_data='santa_get_mywish')],
        [InlineKeyboardButton(text='Пожелания моего дэбила', callback_data='santa_get_recipientwish')]
    ]
    
    keybaord = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.answer(text='Выбери действие', reply_markup=keybaord)


@RouterSanta.callback_query(F.data.startswith('santa'))
async def santaCallback(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_') 
    action = data[1]
    additional_action = data[2]
    
    if action == 'get':
        
        if additional_action == 'recipient':
            await recipient(call)
    
        elif additional_action == 'mywish':
            await mywish(call, state)
        
        elif additional_action == 'recipientwish':
            await recipientwish()

    elif action == 'update':
        
        if additional_action == 'mywish':
            await update()
            
    elif action == 'change':
        if additional_action == 'text':
            await change()

@RouterSanta.message(
    StateFilter(
        SantaFSMGet.GET_TEXT,
        SantaFSMChange.CHANGE_TEXT
    )
)
async def SantaFSM(message:Message, state:FSMContext):
    FSM_santa(message, state)
