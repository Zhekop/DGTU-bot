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
            Database().GenerateTable(table_name="Santa", tg_id="INTEGER", name="STRING", santa_recipient="STRING", my_wish="STRING", photos_id="STRING")


    def GetUsers(self, telegram_id) -> list:
        '''
        
        '''
        pass


    def GetOneUser(self, telegram_id) -> list:
        '''
        вернет все данные о пользователе
        '''
        user_info = Database().GetOne(data='*', table_name='Users', find_param='tg_id', find_value=telegram_id)
        print(user_info)


    def GetFreeUsers(self) -> list:
        Database().GetAll(data='*', table_name='Users', find_param='')


    def GetRecipient(self, my_telegram_id:int|str) -> list:
        self.GetOneUser(telegram_id=my_telegram_id)
        
        
        Database().GetAll(data='*', table_name='Users', find_param='santa', find_value=None)


    def ClearSantaData(self) -> bool:
        pass
