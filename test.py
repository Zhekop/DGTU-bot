from utils import Database 

Database().AddRow(table_name='Users', tg_id=message.from_user.id, tenant_id=321,phone=131231)