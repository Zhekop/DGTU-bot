from utils import SantaRepo
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import asyncio

from utils import Database
# # Database().AddRow(table_name="Santa", tg_id = '123', name='aboba')
# SantaRepo().GetOneUser(te
# legram_id='123')

# print(Database().GetAll(data='*', table_name='Santa', find_param='tg_id', find_value=123), 222)
# print(Database().GetAll(data='id', table_name='Santa', find_param='tg_id', find_value=123), 222)


# print(SantaRepo().GetUsers(find_param='recipient_id', find_value=0))
# print(Database().GetAll(data='tg_id', table_name='Santa', find_param='recipient_id', find_value=0))

# SantaRepo().AddUser(telegram_id=123213213213123, name='Абоба', recipient_id=1016825585)

# recipientwish_info = SantaRepo().GetRecipient(my_telegram_id=773446765)
# wish_my_debil = recipientwish_info[4]

# print(wish_my_debil)


# recipientwish_info = SantaRepo().GetOneUserByTelegramId(telegram_id=773446765)
# wish_my_debil = recipientwish_info[4]

# print(wish_my_debil)

# print(SantaRepo().ClearSantaData())
# print(Database().Replace(table_name='Santa', row='recipient_id', new_value=0, find_param='id', find_value=2))

