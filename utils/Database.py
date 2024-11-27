import sqlite3
from config import db_name


class Database:
    # Singleton Init
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):            
            self.connect = sqlite3.connect(f'{db_name}.db')
            self.cursor = self.connect.cursor()
            self.GenerateTable(table_name='Users', tg_id="INTEGER", name="STRING", santa="STRING")


    def GenerateTable(self, table_name, **kwargs) -> bool:
        '''
        CREATE TABLE IF NOT EXISTS "{table_name}" (
                id INTEGER PRIMARY KEY,
                {values}
            );
        '''
        try:
            values = ''
            rows = list(kwargs.keys())
            params = list(kwargs.values())

            for i in range(len(list(rows))):
                values += f"{rows[i]} {params[i]},"
            else:
                values = values[:-1]

            self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                id INTEGER PRIMARY KEY,
                {values}
            );
            ''')

            self.connect.commit()
            
            return True

        except Exception as e:
            print(f'[sql GenerateTable] {e}')
            return False


    def AddRow(self, table_name, **kwargs) -> bool:
        '''
        INSERT INTO "{table_name}" ({", ".join(list(kwargs.keys()))})
        VALUES ({values})
        '''
        try:
            values = '?,'*(len(kwargs)-1) + '?'

            command = f'''
            INSERT INTO "{table_name}" ({", ".join(list(kwargs.keys()))})
            VALUES ({values})
            '''

            self.cursor.execute(command, tuple(kwargs.values()))
            self.connect.commit()

            return True
        
        except Exception as e:
            print('[sql AddRow]', e)
            return False


    def DeleteRow(self, param, value, table_name) -> bool:
        '''
        DELETE FROM {table_name} WHERE {param} = {value};
        '''
        try:
            command = f'''DELETE FROM {table_name} WHERE {param} = '{value}';'''
            self.cursor.execute(command)
            self.connect.commit()
            return True
        
        except Exception as e:
            print('[sql Delete]', e)
            return False


    def GetOne(self, data, table_name, find_param, find_value) -> str|bool:
        '''
        f'SELECT {data} FROM {table_name} WHERE {find_param} = {find_value}'
        '''
        try:
            query = f'SELECT {data} FROM {table_name} WHERE {find_param} = {find_value}'

            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connect.commit()

            if result == None:
                return False
            
            return result[0]

        except sqlite3.Error as e:
            print(f"[sql GetOne] {e}")
            return False


    def GetAll(self, data, table_name, find_param, find_value) -> str|bool:
        '''
        f'SELECT {data} FROM {table_name} WHERE {find_param} = {find_value}'
        '''
        try:
            query = f'SELECT {data} FROM {table_name} WHERE {find_param} = {find_value}'

            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.connect.commit()
            
            return results

        except sqlite3.Error as e:
            print(f"[sql GetAll] {e}")
            return False


    def GetConnect(self):
        return self.connect


    def GetCursor(self):
        return self.cursor


