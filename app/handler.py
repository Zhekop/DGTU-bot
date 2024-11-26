from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


Routerhandler = Router()

@Routerhandler.message(Command('santa'))
async def getSantaMenu(message:Message):
    inline_keyboard = [
        [InlineKeyboardButton(text='Получатель', callback_data='santa_get_recipient')]
    ]



@Routerhandler.callback_query(F.data.startswith('santa'))
async def santaCallback(call:CallbackQuery):
    data = call.data.split('_')
    
    action = data[1]
    
    if action == 'get':
        additional_action = data[2]
        if additional_action == 'recipient':
            