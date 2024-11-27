import sqlite3
from config import db_name
from .database import Database


class SantaRepo():
    '''
    SantaRepository — акцент на том, что класс отвечает за полноцнный дотуп к функционалу для санты
    '''
    def __init__(self):
        if not hasattr(self, "_initialized"):            
            self.connect = sqlite3.connect(f'{db_name}.db')
            self.cursor = self.connect.cursor()
            Database().GenerateTable(table_name='Users', tg_id="INTEGER", name="STRING", name_recipient="STRING")


    def GetUsers(self):
        pass


    def GetOneUser(self, user_id):
        pass


    def GetFreeUsers(self):
        Database().GetAll(data='*', table_name='Users', find_param='')

