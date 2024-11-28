from utils import SantaRepo, Database

# # Database().AddRow(table_name="Santa", tg_id = '123', name='aboba')
# SantaRepo().GetOneUser(telegram_id='123')

# print(Database().GetAll(data='*', table_name='Santa', find_param='tg_id', find_value=123), 222)
# print(Database().GetAll(data='id', table_name='Santa', find_param='tg_id', find_value=123), 222)


SantaRepo().GetOneUser(telegram_id=123)
