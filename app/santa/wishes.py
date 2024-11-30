import random

from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from utils import SantaRepo, SantaFSMGet, SantaFSMChange


async def recipient(call:CallbackQuery):
    '''
    получение моего дебила
    '''
    await call.answer()
    
    name = f'{call.message.from_user.full_name}'
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id, name=name):
        await call.message.answer(text=text)
        return

    recipient_info = SantaRepo().GetRecipient(my_telegram_id=call.from_user.id)
    
    if not recipient_info:
        recipients = SantaRepo().GetFreeUsers() # получаем список дэбилов
        
        if len(recipients) == 1:
            if recipients[0][1] == call.from_user.id:
                await call.message.answer('Анлаки')
                return

        recipient_user = random.choice(recipients) # выбираем одного из этих дэбилов

        while recipient_user[1] == call.from_user.id:
            recipient_user = random.choice(recipients) # выбираем одного из этих дэбилов

        SantaRepo().UpdateUserDataByUserID(update_param='recipient_id', new_value=recipient_user[1], user_id=call.from_user.id)
        return
    
    inline_keyboard = [
        [InlineKeyboardButton(text='Пожелания моего дэбила', callback_data='santa_get_recipientwish')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    
    await call.message.answer(text=f'Твой получатель: {recipient_info[2]}', reply_markup=keyboard)


async def mywish(call: CallbackQuery, state: FSMContext):
    await call.answer()

    name = f'{call.message.from_user.full_name}'
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id, name=name):
        await call.message.answer(text=text)
        return

    await call.message.answer('Напишите ваши пожелания:')

    await state.set_state(SantaFSMGet.GET_TEXT)


async def recipientwish(call: CallbackQuery, state:FSMContext):
    await call.answer()
    
    name = f'{call.message.from_user.full_name}'
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id, name=name):
        await call.message.answer(text=text)
        return
    
    recipientwish_info = SantaRepo().GetRecipient(my_telegram_id=call.message.from_user.id)
    wish_my_debil = recipientwish_info[4]

    await call.message.answer(f'Пожелания моего дэбила: {wish_my_debil}')


async def FSM_santa(message: Message, state: FSMContext):
    '''

    '''
    now_state = state.get_state()
    
    if await now_state == SantaFSMGet.GET_TEXT or now_state == SantaFSMChange.CHANGE_TEXT:
        
        await state.update_data(data={"mywish": message.text})
        
        inline_keyboard = [
            [InlineKeyboardButton(text='Да', callback_data='santa_update_mywish')],
            [InlineKeyboardButton(text='Изменить', callback_data='santa_change_text')]
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        await message.answer('Вы уверены в своём пожелании?', reply_markup=keyboard)


async def update(call:CallbackQuery, state: FSMContext, additional_action:str):
    '''
    
    '''
    await call.answer()

    if additional_action == 'mywish':
        data = await state.get_data()
        
        mywish_text = data.get(additional_action)
        
        SantaRepo().UpdateUserDataByUserID(update_param='my_wish', new_value=mywish_text, user_id=call.from_user.id)

    await call.message.answer('Пожелание добавлено!')


async def change(call:CallbackQuery, state: FSMContext, additional_action:str):
    '''
    
    '''

    if additional_action == 'text':
        await state.set_state(SantaFSMChange.CHANGE_TEXT)
        await call.message.answer('Напишите ваши пожелания:')


def check(chat_id, user_id, name) -> str|bool:
    '''
    \n False - если все гуд
    _str_ - если есть ошибка
    '''
    
    if not(SantaRepo().GetOneUserByTelegramId(telegram_id=user_id)):
        if SantaRepo().AddUser(telegram_id=user_id, name=name):
            print(f'[SantaRepo] User was added')        
        
    if chat_id != user_id:
        return 'Не в этом чате' #проверить
    
    return False 


