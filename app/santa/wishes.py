from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from .handler import RouterSanta

from utils import SantaRepo
from utils.FSM import FSM_get

async def recipient(call:CallbackQuery):
    '''
    получение моего дебила
    '''
    await call.answer()
    
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id):
        await call.message.answer(text=text)
        return

    recipient_info = SantaRepo().GetRecipient()


async def mywish(call: CallbackQuery, state: FSMContext):
    await call.answer()
    
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id):
        await call.message.answer(text=text)
        return
    
    await call.message.answer('Напишите ваши пожелания')

    await state.set_state(FSM_get.GET_TEXT)

async def recipientwish(call: CallbackQuery, state:FSMContext):
    await call.answer()
    
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id):
        await call.message.answer(text=text)
        return


async def FSM_santa(message: Message, state: FSMContext):
    await state.update_data(wish=message.text)
    inline_keyboard = [
        [InlineKeyboardButton(text='Да', callback_data='santa_yes')],
        [InlineKeyboardButton(text='Изменить', callback_data='santa_change')]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.answer('Вы уверены в своём пожелании?', reply_markup=keyboard)
    
    await state.set_state(FSM_get.GET_ACCEPT)


async def FSM_santa_wish(message: Message, state: FSMContext):
    data = await state.get_data()
    wish = data.get('wish')




async def check(chat_id, user_id) -> str|bool:
    '''
    \n False - если все гуд
    \n _str_ - если есть ошибка
    '''
    if chat_id == user_id:
        return