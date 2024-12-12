import random

from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from utils import SantaRepo, SantaFSMGet, SantaFSMChange, keyboard_main_menu, recipient_keyboard, mywish_keybaord, keyboard_back_to_menu, change_recipient_keyboard
from config import bot
from asyncio import sleep

async def recipient(call:CallbackQuery):
    '''
    получение чела кому я буду дарить что-то
    '''
    await call.answer()
    
    name = f'{call.from_user.full_name}'
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id, name=name):
        await call.message.answer(text=text)
        return

    recipient_info = SantaRepo().GetRecipient(my_telegram_id=call.from_user.id)
    
    if not recipient_info:
        recipients = SantaRepo().GetFreeUsers() # получаем список дэбилов
        
        if len(recipients) == 1:
            if recipients[0][1] == call.from_user.id:
                await call.message.edit_text('Для тебя не хватает пары(\nАнлаки')
                await nice_sleep(time=3, text='Главное меню вернется через ', message=call.message, is_del=False)
                await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboard_main_menu)
                return

        recipient_user = random.choice(recipients) # выбираем одного из доступных получателей

        while recipient_user[1] == call.from_user.id:
            recipient_user = random.choice(recipients) # повторяем если тебе выпал ты сам

        SantaRepo().UpdateUserDataByUserID(update_param='recipient_id', new_value=recipient_user[1], user_id=call.from_user.id)
        recipient_info = SantaRepo().GetRecipient(my_telegram_id=call.from_user.id)
    
    await call.message.edit_text(text=f'Твой получатель: {recipient_info[2]}', reply_markup=recipient_keyboard)


async def change_recipient(call: CallbackQuery, additional_action:str):
    '''
    смена получателя
    '''
    await call.answer()

    if additional_action == 'change':
        can_rerol = SantaRepo().GetOneUserByTelegramId(telegram_id=call.from_user.id)
        how_many = can_rerol[4]

        if how_many == 0:
            await call.message.edit_text('Больше нельзя менять получателя')
            await nice_sleep(time=3, text='Главное меню вернется через ', message=call.message, is_del=False)
            await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboard_main_menu)

        else: 
            await call.message.edit_text(text=f'❗️ВНИМАНИЕ❗️\nТы можешь поменять получателя ещё {how_many} раз(а)\nТочно меняем?',
                                    reply_markup=change_recipient_keyboard)
        

async def confirmed_change_recipient(call: CallbackQuery, additional_action:str):
    '''
    удаляем действующего получателя
    '''

    if additional_action == 'confrim':
        can_rerol = SantaRepo().GetOneUserByTelegramId(telegram_id=call.from_user.id)
        how_many = can_rerol[4]
        SantaRepo().UpdateUserDataByUserID(update_param='can_rerol', new_value=how_many-1, user_id=call.from_user.id)

        SantaRepo().UpdateUserDataByUserID(update_param='recipient_id', new_value=None, user_id=call.from_user.id)
        await recipient(call)


async def mywish(call: CallbackQuery, state: FSMContext):
    await call.answer()

    name = f'{call.from_user.full_name}'
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id, name=name):
        await call.message.answer(text=text)
        return

    my_info = SantaRepo().GetOneUserByTelegramId(telegram_id=call.from_user.id)
    my_wish = my_info[5]

    if my_wish == None:
        message = await call.message.edit_text('Напишите ваши пожелания:')

        await state.set_state(SantaFSMGet.GET_TEXT)
        await state.update_data(data={'message_id':message.message_id})
        return

    answer_text=f'Ваше пожелание: \n{my_wish}'

    medias = my_info[6]

    if medias == None:
        await call.message.edit_text(text=answer_text, reply_markup=mywish_keybaord)
        return 
    
    media = []
    for i in medias:
        if media == []:
            media.append(InputMediaPhoto(media=i, caption=answer_text))
        media.append(InputMediaPhoto(media=i))
    else:  
        await call.message.edit_media(media=media, reply_markup=mywish_keybaord)


async def recipientwish(call: CallbackQuery):
    await call.answer()
    
    name = f'{call.from_user.full_name}'
    if text:= check(chat_id=call.message.chat.id, user_id=call.from_user.id, name=name):
        await call.message.answer(text=text)
        return
    
    recipientwish_info = SantaRepo().GetRecipient(my_telegram_id=call.from_user.id)
    if not recipientwish_info:
        await call.message.edit_text(text='У вас нет получателя')
        await nice_sleep(time=3, text='Главное меню вернется через ', message=call.message, is_del=False)
        await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboard_main_menu)
        return

    wish_my_recipient = recipientwish_info[5]
    medias = recipientwish_info[6]

    if wish_my_recipient == None:
        answer_text = 'У вашего получателя нет пожеланий.\nОтправить ему просьбу добавить пожелание?'
    else:
        answer_text = f'Пожелания моего дэбила: {wish_my_recipient}'

    if medias == None:
        await call.message.edit_text(answer_text, reply_markup=keyboard_back_to_menu)
        return
    
    media = []
    for i in medias:
        if media == []:
            media.append(InputMediaPhoto(media=i, caption=answer_text))
        media.append(InputMediaPhoto(media=i))
        
    else:
        await call.message.edit_media(media=media, reply_markup=mywish_keybaord)


async def FSM_santa(message: Message, state: FSMContext):
    '''

    '''
    now_state = await state.get_state()

    if now_state == SantaFSMGet.GET_TEXT or now_state == SantaFSMChange.CHANGE_TEXT:
        
        await state.update_data(data={"mywish": message.text})
        message_id = await state.get_value(key="message_id")
        
        inline_keyboard = [
            [InlineKeyboardButton(text='Да', callback_data='santa_update_mywish')],
            [InlineKeyboardButton(text='Изменить', callback_data='santa_change_text')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        
        await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        await message.answer(text=f'Ваше пожелание:\n{message.text}\nВы уверены в своём пожелании?', reply_markup=keyboard)


async def update(call:CallbackQuery, state: FSMContext, additional_action:str):
    '''
    
    '''
    await call.answer()

    if additional_action == 'mywish':
        data = await state.get_data()
        
        mywish_text = data.get(additional_action)
        
        SantaRepo().UpdateUserDataByUserID(update_param='my_wish', new_value=mywish_text, user_id=call.from_user.id)

    await call.message.edit_text('Пожелание добавлено!')
    await nice_sleep(time=3, text='Главное меню вернется через ', message=call.message, is_del=False)
    await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboard_main_menu)


async def change(call:CallbackQuery, state:FSMContext, additional_action:str):
    '''
    
    '''

    if additional_action == 'text':

        await state.update_data(data={'message_id':call.message.message_id})
        await call.message.edit_text('Напишите ваши пожелания:')
        await state.set_state(SantaFSMChange.CHANGE_TEXT)


async def setFsm(call:CallbackQuery, state:FSMContext, additional_action:str):
    if additional_action == 'changemywishtext':
        await state.set_state(SantaFSMGet.GET_TEXT)
        await call.message.answer(text='Введите новое пожелание')

    elif additional_action == 'changemywishphoto':
        await state.set_state(SantaFSMGet.GET_PHOTO)
        await call.message.answer(text='Введите новые картинки')

    # elif additional_action == '':

    # elif additional_action == '':


async def backToMenu(call:CallbackQuery):
    await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboard_main_menu)


def check(chat_id, user_id, name) -> str|bool:
    '''
    \n False - если все гуд
    _str_ - если есть ошибка
    '''
    
    if not(SantaRepo().GetOneUserByTelegramId(telegram_id=user_id)):
        if SantaRepo().AddUser(telegram_id=user_id, name=name):
            print(f'[SantaRepo] User was added')        
        
    if chat_id != user_id:
        return 'Писать надо в лс сука' #проверить
    
    return False 


async def nice_sleep(time:int, text:str, message:Message, is_del:bool = True):

    digits_with_emojis = (
    (0, "0️⃣"),  # Ноль
    (1, "1️⃣"),  # Один
    (2, "2️⃣"),  # Два
    (3, "3️⃣"),  # Три
    (4, "4️⃣"),  # Четыре
    (5, "5️⃣"),  # Пять
    (6, "6️⃣"),  # Шесть
    (7, "7️⃣"),  # Семь
    (8, "8️⃣"),  # Восемь
    (9, "9️⃣")   # Девять
)
    try:
        for i in range(1, time+1):
            await sleep(1)
            await_text = f'{text} {digits_with_emojis[time+1-i][1]}'
            await message.edit_text(text=await_text)
        else:
            await sleep(1)
            if is_del:
                await message.delete()
        return True
    
    except Exception as e:
        return False
