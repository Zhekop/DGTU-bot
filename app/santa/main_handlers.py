from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from utils import Database, SantaRepo, keyboard_main_menu
from utils.FSM import SantaFSMGet, SantaFSMChange

from .handlers import (backToMenu, recipient, change_recipient, mywish, recipientwish, 
                       FSM_santa, update, change, setFsm, check, confirmed_change_recipient, request)

RouterSanta = Router()


@RouterSanta.message(Command('santa'))
async def getSantaMenu(message:Message):
    
    name = f'{message.from_user.full_name}'
    if text:=check(chat_id=message.chat.id, user_id=message.from_user.id, name=name):
        await message.answer(text=text)
        return

    await message.answer(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboard_main_menu)


@RouterSanta.callback_query(F.data.startswith('santa'))
async def santaCallback(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_') 
    action = data[1]

    if action == 'backtomenu':
        await backToMenu(call)
        return

    additional_action = data[2]

    if action == 'get':

        if additional_action == 'recipient':
            await recipient(call)
    
        elif additional_action == 'mywish':
            await mywish(call, state)
        
        elif additional_action == 'recipientwish':
            await recipientwish(call)

    elif action == 'update':
        await update(call, state, additional_action=additional_action)
            
    elif action == 'change':
        await change(call, state, additional_action=additional_action)
    
    elif action == 'setfsm':
        await setFsm(call, state, additional_action)
    
    elif action == 'request':
        await request(call, additional_action)

    elif action == 'res':
        await change_recipient(call, additional_action=additional_action)

    elif action == 'reschange':
        await confirmed_change_recipient(call, additional_action=additional_action)


@RouterSanta.message(
    StateFilter(
        SantaFSMGet.GET_TEXT,
        SantaFSMChange.CHANGE_TEXT
    )
)
async def SantaFSM(message:Message, state:FSMContext):
    await FSM_santa(message, state)


