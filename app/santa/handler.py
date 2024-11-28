from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from utils import Database, SantaRepo
from utils.FSM import FSM_get

from .wishes import recipient, mywish, recipientwish, FSM_santa, FSM_santa_wish

RouterSanta = Router()


@RouterSanta.message(Command('santa'))
async def getSantaMenu(message:Message):
    inline_keyboard = [
        [InlineKeyboardButton(text='Получатель', callback_data='santa_get_recipient')],
        [InlineKeyboardButton(text='Мои пожелания', callback_data='santa_get_mywish')],
        [InlineKeyboardButton(text='Пожелания моего дэбила', callback_data='santa_get_recipientwish')]
    ]
    
    keybaord = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.answer(text='Выбери действие', reply_markup=keybaord)


@RouterSanta.callback_query(F.data.startswith('santa'))
async def santaCallback(call: CallbackQuery):
    data = call.data.split('_') 
    action = data[1]
    
    if action == 'get':
        additional_action = data[2]
        
        if additional_action == 'recipient':
            await recipient()
    
        elif additional_action == 'mywish':
            await mywish()
        
        elif additional_action == 'recipientwish':
            await recipientwish()


@RouterSanta.message(StateFilter(
    FSM_get.GET_TEXT
))
async def SantaFSM():
    FSM_santa()


@RouterSanta.callback_query(F.data.startswith('santa'), StateFilter(
        FSM_get.GET_ACCEPT
))
async def sants_wish_FSM(call: CallbackQuery):
    data = call.data.split('_') 
    action = data[1]
    
    if action == 'yes':
        await FSM_santa_wish

    elif action == 'change':
        await 