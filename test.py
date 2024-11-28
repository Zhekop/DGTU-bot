from utils import SantaRepo, Database

Database().AddRow(table_name="Users", tg_id = '123', name='aboba', santa=0)
SantaRepo().GetOneUser(telegram_id='123')