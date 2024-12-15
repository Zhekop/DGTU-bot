import random

from aiogram import Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from utils import SantaRepo, SantaFSMGet, SantaFSMChange, keyboards
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
                await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboards.keyboard_main_menu)
                return

        recipient_user = random.choice(recipients) # выбираем одного из доступных получателей

        while recipient_user[1] == call.from_user.id:
            recipient_user = random.choice(recipients) # повторяем если тебе выпал ты сам

        SantaRepo().UpdateUserDataByTelegramID(update_param='recipient_id', new_value=recipient_user[1], user_id=call.from_user.id)
        recipient_info = SantaRepo().GetRecipient(my_telegram_id=call.from_user.id)

    await call.message.edit_text(text=f'Твой получатель: {recipient_info[2]}', reply_markup=keyboards.recipient_keyboard)


async def show_can_rerol_to_user(call: CallbackQuery, additional_action:str):
    '''
    показывает количество попыток
    '''
    await call.answer()

    if additional_action == 'show':
        can_rerol = SantaRepo().GetOneUserByTelegramId(telegram_id=call.from_user.id)
        how_many = can_rerol[4]

        if how_many == 0:
            await call.message.edit_text('Больше нельзя менять получателя')
            await nice_sleep(time=3, text='Главное меню вернется через ', message=call.message, is_del=False)
            await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboards.keyboard_main_menu)

        else: 
            await call.message.edit_text(text=f'❗️ВНИМАНИЕ❗️\nТы можешь поменять получателя ещё {how_many} раз(а)\nТочно меняем?',
                                    reply_markup=keyboards.change_recipient_keyboard)


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

    medias:str = my_info[6]

    if medias == None:
        await call.message.edit_text(text=answer_text, reply_markup=keyboards.mywish_keybaord)
        return

    medias_list = medias.split(' ')
    media = []
    for i in medias_list:
        if media == []:
            media.append(InputMediaPhoto(media=i, caption=answer_text))
            continue
        media.append(InputMediaPhoto(media=i))
    else:
        try:
            await call.message.delete()
            message = await call.message.answer_media_group(media=media)
            message = message[0]
            await message.edit_reply_markup(reply_markup=keyboards.mywish_keybaord)
        except Exception as e:
            print(e)


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
        await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboards.keyboard_main_menu)
        return

    wish_my_recipient = recipientwish_info[5]
    photo = recipientwish_info[6]

    if wish_my_recipient == None:
        answer_text = 'У вашего получателя нет пожеланий.\nОтправить ему просьюу добавить пожелание?'
        await call.message.edit_text(text=answer_text, reply_markup=keyboards.recipientwish_keyboard)
        return
    
    answer_text = f'Пожелания моего получателя: {wish_my_recipient}'

    if photo == None:
        await call.message.edit_text(answer_text, reply_markup=keyboards.keyboard_back_to_menu)
        return
    
    else:
        await call.message.delete()
        await call.message.answer_photo(photo=photo, caption=answer_text, reply_markup=keyboards.keyboard_back_to_menu)


async def FSM_santa(message: Message, state: FSMContext):
    '''

    '''
    now_state = await state.get_state()
    
    if now_state == SantaFSMGet.GET_TEXT or now_state == SantaFSMChange.CHANGE_TEXT:

        if message.text.lower() in ['стоп','отмена','нет','хватит','остановить']:
            message_id = await state.get_value(key="message_id")
            await state.clear()
            await nice_sleep(time=3, text='Остановлено, главное меню вернется через ', bot=message.bot, is_del=False, message_id=message_id, chat_id=message.chat.id)
            await bot.edit_message_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', chat_id=message.chat.id, message_id=message_id, reply_markup=keyboards.keyboard_main_menu)
            return

        await state.update_data(data={"mywish": message.text})
        message_id = await state.get_value(key="message_id")

        inline_keyboard = [
            [InlineKeyboardButton(text='Да', callback_data='santa_update_mywish')],
            [InlineKeyboardButton(text='Изменить', callback_data='santa_change_text')]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        
        answer_text = f'Ваше пожелание:\n{message.text}\nВы уверены в своём пожелании?'
        await message.delete()
        await message.bot.edit_message_text(text=answer_text, chat_id=message.chat.id, message_id=message_id, reply_markup=keyboard)

    elif now_state == SantaFSMGet.GET_PHOTO or now_state == SantaFSMChange.CHANGE_PHOTO: 
        try:
            await state.update_data(data={"photos_id": message.photo[-1].file_id})
            message_id = await state.get_value(key="message_id")

            inline_keyboard = [
                [InlineKeyboardButton(text='Да', callback_data='santa_update_photo')],
                [InlineKeyboardButton(text='Изменить', callback_data='santa_change_photo')]
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

            answer_text = "Ваше фото\nПодтвердить?"
            answer_media = InputMediaPhoto(media=message.photo[-1].file_id, caption=answer_text)
            await message.delete()
            await message.bot.edit_message_media(media=answer_media, chat_id=message.chat.id, message_id=message_id, reply_markup=keyboard)
            return
        
        except Exception as e:
            await state.clear()
            message = await message.answer(text='Ты че, сказано же присылай одну фотку')
            print(e, message.from_user.full_name)
            return


async def update(call:CallbackQuery, state: FSMContext, additional_action:str):
    '''
    
    '''
    await call.answer()

    if additional_action == 'mywish':
        
        mywish_text = await state.get_value(key=additional_action)
        
        SantaRepo().UpdateUserDataByTelegramID(update_param='my_wish', new_value=mywish_text, user_id=call.from_user.id)

        await call.message.edit_text('Пожелание добавлено!')
        await nice_sleep(time=3, text='Главное меню вернется через ', message=call.message, is_del=False)
        await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboards.keyboard_main_menu)
        return

    elif additional_action == 'photo':

        photos_id = await state.get_value(key='photos_id')
        SantaRepo().UpdateUserDataByTelegramID(update_param='photos_id', new_value=photos_id, user_id=call.from_user.id)

        await call.message.delete()
        message = await call.message.answer('Пожелание добавлено!')

        await nice_sleep(time=3, text='Главное меню вернется через ', message=message, is_del=False)
        await message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboards.keyboard_main_menu)


async def change(call:CallbackQuery, state:FSMContext, additional_action:str):
    '''
    
    '''
    await call.answer()
    if additional_action == 'text':

        await state.update_data(data={'message_id':call.message.message_id})
        await call.message.edit_text('Напишите ваши пожелания:')
        await state.set_state(SantaFSMChange.CHANGE_TEXT)
    
    elif additional_action == 'photo':
        
        await state.update_data(data={'message_id':call.message.message_id})
        await call.message.delete()
        await call.message.answer('Пришли новую фотку:')
        await state.set_state(SantaFSMChange.CHANGE_PHOTO)
    
    elif additional_action == 'recipient':
        can_rerol = SantaRepo().GetOneUserByTelegramId(telegram_id=call.from_user.id)
        how_many = can_rerol[4]
        
        SantaRepo().UpdateUserDataByTelegramID(update_param='can_rerol', new_value=how_many-1, user_id=call.from_user.id)
        SantaRepo().UpdateUserDataByTelegramID(update_param='recipient_id', new_value=None, user_id=call.from_user.id)
        await recipient(call)
        

async def setFsm(call:CallbackQuery, state:FSMContext, additional_action:str):
    if additional_action == 'changemywishtext':
        await state.set_state(SantaFSMGet.GET_TEXT)
        await state.update_data(data={'message_id':call.message.message_id})
        await call.message.edit_text(text='Введите новое пожелание')

    elif additional_action == 'changemywishphoto':
        await state.set_state(SantaFSMGet.GET_PHOTO)
        await call.message.delete()
        message = await call.message.answer(text='Введите новую картинку')
        await state.update_data(data={'message_id':message.message_id})

    return
    # elif additional_action == '':

    # elif additional_action == '':


async def backToMenu(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboards.keyboard_main_menu)


async def request(call: CallbackQuery, addidional_action: str):
    await call.answer()
    if addidional_action == 'recipientwish':
        recipient_info = SantaRepo().GetRecipient(my_telegram_id=call.from_user.id)
        chat_id = recipient_info[1]
        await call.bot.send_message(chat_id=chat_id, text='[SANTA] Заполни сво(Ё) пожелания.')
        await nice_sleep(time=3, text='Главное меню вернется через ', message=call.message, is_del=False)
        await call.message.edit_text(text='🎅Это раздел санты\nВыбери что ты хочешь узнать)', reply_markup=keyboards.keyboard_main_menu)
        

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


async def nice_sleep(time: int, text: str, message: Message = None, is_del: bool = True, bot: Bot = None, message_id: str|int = None, chat_id: str|int = None):

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
            answer_text = f'{text} {digits_with_emojis[time+1-i][1]}'
            if bot:
                await bot.edit_message_text(text=answer_text, chat_id=chat_id, message_id=message_id)
                continue    
            await message.edit_text(text=answer_text)
        else:
            await sleep(1)
            if is_del:
                if bot:
                    await bot.delete_message(chat_id=chat_id, message_id=message_id)
                    return True
                await message.delete()
        return True
    
    except Exception as e:
        print(e)
        return False
