from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from utils import SantaRepo, SantaFSMGet, SantaFSMChange


async def recipient(call:CallbackQuery):
    '''
    получение моего дебила
    '''
    await call.answer()
    
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id):
        await call.message.answer(text=text)
        return

    recipient_info = SantaRepo().GetRecipient(my_telegram_id=call.message.from_user.id)
    
    inline_keyboard = [
        [InlineKeyboardButton(text='Пожелания моего дэбила', callback_data='santa_get_recipientwish')]
    ]
    keybaord = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    
    await call.message.answer(text=f'{recipient_info[2]}', reply_markup=keybaord)


async def mywish(call: CallbackQuery, state: FSMContext):
    await call.answer()

    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id):
        await call.message.answer(text=text)
        return

    await call.message.answer('Напишите ваши пожелания:')

    await state.set_state(SantaFSMGet.GET_TEXT)


async def recipientwish(call: CallbackQuery, state:FSMContext):
    await call.answer()
    
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id):
        await call.message.answer(text=text)
        return
    
    recipientwish_info = SantaRepo().GetRecipient(my_telegram_id=call.message.from_user.id)
    wish_my_debil = recipientwish_info[1]

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
    if additional_action == 'mywish':
        data = await state.get_data()
        
        mywish_text = data.get(additional_action)
        
        SantaRepo().UpdateUserDataByUserID(update_param='my_wish', new_value=mywish_text, user_id=call.from_user.id)


async def change(call:CallbackQuery, state: FSMContext, additional_action:str):
    '''
    
    '''

    if additional_action == 'text':
        await state.set_state(SantaFSMChange.CHANGE_TEXT)
        await call.message.answer('Напишите ваши пожелания:')


async def check(chat_id, user_id) -> str|bool:
    '''
    \n False - если все гуд
    _str_ - если есть ошибка
    '''
    if chat_id == user_id:
        return