from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import config
from utils import keyboard_main_menu, SantaFSMGet, SantaFSMChange

from .handlers import (backToMenu, recipient, mywish, recipientwish, 
                       FSM_santa, update, change, setFsm, check, show_can_rerol_to_user, request)

RouterSanta = Router()


@RouterSanta.message(Command('santa'))
async def getSantaMenu(message:Message):
    
    name = f'{message.from_user.full_name}'
    if text:=check(chat_id=message.chat.id, user_id=message.from_user.id, name=name):
        await message.answer(text=text)
        return

    await message.answer(text=config.main_text, reply_markup=keyboard_main_menu)


@RouterSanta.callback_query(F.data.startswith('santa'))
async def santaCallback(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_') 
    action = data[1]
    print(call.from_user.full_name, action, call.message.date.date())
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
        await update(call, state, additional_action)
            
    elif action == 'change':
        await change(call, state, additional_action)
    
    elif action == 'setfsm':
        await setFsm(call, state, additional_action)
    
    elif action == 'request':
        await request(call, additional_action)

    elif action == 'reschange':
        await show_can_rerol_to_user(call, additional_action)


@RouterSanta.message(
    StateFilter(
        SantaFSMGet.GET_TEXT,
        SantaFSMChange.CHANGE_TEXT,
        SantaFSMGet.GET_PHOTO,
        SantaFSMChange.CHANGE_PHOTO,
    )
)
async def SantaFSM(message:Message, state:FSMContext):
    await FSM_santa(message, state)


