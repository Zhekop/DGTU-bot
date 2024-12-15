import sqlite3
from config import db_name
from .Database import Database


class SantaRepo:
    '''
    SantaRepository — акцент на том, что класс отвечает за полноцнный дотуп к функционалу для санты
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):            
            self.connect = Database().GetConnect()
            self.cursor = Database().GetCursor()
            Database().GenerateTable(table_name="Santa", tg_id="INTEGER", name="STRING", recipient_id="INTEGER DEFAULT 0", can_rerol = "INT DEFAULT 2", my_wish="STRING", photos_id="STRING")


    def AddUser(self, telegram_id, name, recipient_id=0) -> bool:
        '''
        Добавляет пользователя
        '''
        return Database().AddRow(table_name='Santa', tg_id=telegram_id, name=name, recipient_id=recipient_id)
        

    def GetUsers(self, find_param, find_value) -> list[tuple]:
        '''
        Возвращает всех пользователей по искомому параметру
        '''
        return Database().GetAll(data='*', table_name='Santa', find_param=find_param, find_value=find_value)


    def UpdateUserDataByTelegramID(self, update_param, new_value, user_id) -> bool:
        '''
        Обновляет параметр у пользователя по Telegram ID
        '''
        return Database().Update(table_name='Santa', row=update_param, new_value=new_value, find_param='tg_id', find_value=user_id)
    
    
    def GetOneUserByTelegramId(self, telegram_id) -> list|bool:
        '''
        вернет все данные о пользователе по tg_id
        '''
        return Database().GetOne(data='*', table_name='Santa', find_param='tg_id', find_value=telegram_id)


    def GetOneUserById(self, idd) -> list|bool:
        '''
        вернет все данные о пользователе по его ID (idd)
        '''
        return Database().GetOne(data='*', table_name='Santa', find_param='id', find_value=idd)


    def GetFreeUsers(self) -> list|bool:
        '''
    \n Вернет всех "свободных" пользователей
    \n Тех у кого нет санты
        '''
        all_users = self.Count()
        
        # user_wishout_recipient_id = Database().GetAll(data='tg_id', table_name='Santa', find_param='recipient_id', find_value=0)
        # len_user_wishout_recipient = len(user_wishout_recipient_id) #юзеры которые ничего не получают (кол-во)
        
        users = []
        
        for i in range(1, all_users+1):

            try:
                user_tg_id = self.GetOneUserById(idd=i)[1]
                user = self.GetUsers(find_param='recipient_id', find_value=user_tg_id)
            except:
                return False
            
            if user != []:
                continue
            
            users.append(self.GetOneUserByTelegramId(telegram_id=user_tg_id))
            
        else:
            return users
        

    def GetRecipient(self, my_telegram_id:int|str) -> list|bool:
        '''
        \n Возвращает данные получателя, по Telegram ID его санты
        \n Если у Санты нет получателя, вернется False
        '''
        my_info = self.GetOneUserByTelegramId(telegram_id=int(my_telegram_id))
        recipient_tg_id = my_info[3]
        
        if recipient_tg_id:
            recipient_info = self.GetOneUserByTelegramId(telegram_id=recipient_tg_id)
            return recipient_info
        
        return False


    def ClearSantaData(self) -> bool:
        '''
        Очищается таблица Users ПОЛНОСТЬЮ
        '''
        all_users = self.Count()
        try:
            for i in range(1, all_users+1):
                Database().DeleteRow(table_name="Santa", param='id', value=i)
            else:
                return True
        except:
            return False
    
    def RowCount(self)-> int|bool: 
        '''
        кол-во строк в таблице Santa
        '''
        return Database().RowCount(table_name='Santa')
    
    
