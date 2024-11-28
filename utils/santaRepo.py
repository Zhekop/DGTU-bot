import sqlite3
from config import db_name
from .database import Database


class SantaRepo():
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
            Database().GenerateTable(table_name="Santa", tg_id="INTEGER", name="STRING", recipient_id="INTEGER DEFAULT  0", my_wish="STRING", photos_id="STRING")


    def AddUser(self, telegram_id, name) -> bool:
        return Database().AddRow(table_name='Santa', tg_id=telegram_id, name=name)
        

    def GetUsers(self, telegram_id) -> list:
        '''
        
        '''
        pass


    def UpdateUserDataByUserID(self, update_param, new_value, user_id) -> bool:
        res = Database().Replace(table_name='Santa', row=update_param, new_value=new_value, find_param='tg_id', find_value=user_id)
        return res
    
    
    def GetOneUser(self, telegram_id) -> list|bool:
        '''
        вернет все данные о пользователе по tg_id
        '''
        return Database().GetOne(data='*', table_name='Santa', find_param='tg_id', find_value=telegram_id)


    def GetFreeUsers(self) -> list:
        Database().GetAll(data='*', table_name='Santa', find_param='')


    def GetRecipient(self, my_telegram_id:int|str) -> list|bool:
        print(my_telegram_id)
        my_info = self.GetOneUser(telegram_id=int(my_telegram_id))
        
        recipient_tg_id = my_info[3]
        
        if recipient_tg_id:
            recipient_info = self.GetOneUser(telegram_id=recipient_tg_id)
            # recipient_info = Database().GetOne(data='*', table_name='Santa', find_param='recipient_id', find_value=recipient_tg_id)
            return recipient_info
        
        return False


    def ClearSantaData(self) -> bool:
        pass
