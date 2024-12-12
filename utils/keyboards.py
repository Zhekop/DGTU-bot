from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_keyboard_main_menu = [
        [InlineKeyboardButton(text='Мой получатель', callback_data='santa_get_recipient')],
        [InlineKeyboardButton(text='Мои пожелания', callback_data='santa_get_mywish')],
        [InlineKeyboardButton(text='Пожелания моего получателя', callback_data='santa_get_recipientwish')]
    ]
keyboard_main_menu = InlineKeyboardMarkup(inline_keyboard=inline_keyboard_main_menu)


inline_keyboard_back_to_menu = [
    [InlineKeyboardButton(text='Назад в меню', callback_data='santa_backtomenu')]
]
keyboard_back_to_menu = InlineKeyboardMarkup(inline_keyboard=inline_keyboard_back_to_menu)


recipient_inline_keyboard = [
    [InlineKeyboardButton(text='Пожелания моего получателя', callback_data='santa_get_recipientwish')],
    [InlineKeyboardButton(text='Изменить получателя', callback_data='santa_res_change')],
    inline_keyboard_back_to_menu[0] # кнопка "назад в меню"
]
recipient_keyboard = InlineKeyboardMarkup(inline_keyboard=recipient_inline_keyboard)

change_recipient_inline_keyboard = [
    [InlineKeyboardButton(text='Да, меняем', callback_data='santa_reschange_confrim')],
    [InlineKeyboardButton(text='Нет, оставим', callback_data='santa_get_recipient')],
    inline_keyboard_back_to_menu[0] # кнопка "назад в меню"
]
change_recipient_keyboard = InlineKeyboardMarkup(inline_keyboard=change_recipient_inline_keyboard)

mywish_inline_keybaord = [
        [InlineKeyboardButton(text='Изменить пожелание', callback_data='santa_setfsm_changemywishtext')],
        [InlineKeyboardButton(text='Изменить картинки/картинку', callback_data='santa_setfsm_changemywishphoto')],
        inline_keyboard_back_to_menu[0] # кнопка "назад в меню"
    ]
mywish_keybaord = InlineKeyboardMarkup(inline_keyboard=mywish_inline_keybaord)
