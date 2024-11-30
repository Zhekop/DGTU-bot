from utils import SantaRepo, Database
import random

# # Database().AddRow(table_name="Santa", tg_id = '123', name='aboba')
# SantaRepo().GetOneUser(telegram_id='123')

# print(Database().GetAll(data='*', table_name='Santa', find_param='tg_id', find_value=123), 222)
# print(Database().GetAll(data='id', table_name='Santa', find_param='tg_id', find_value=123), 222)


# print(SantaRepo().GetUsers(find_param='recipient_id', find_value=0))
# print(Database().GetAll(data='tg_id', table_name='Santa', find_param='recipient_id', find_value=0))

# SantaRepo().AddUser(telegram_id=123213213213123, name='Абоба', recipient_id=1016825585)

# Я СДЕЛЯЛЬ
recipient = SantaRepo().GetFreeUsers() # получаем список дэбилов
recipient_user = random.choice(recipient) # выбираем одного из этих дэбилов

f = 
if recipient_user[1] == 

SantaRepo().UpdateUserDataByUserID('recipient_id', recipient_user[1], 773446765)
print(recipient_user[1])


