import sqlite3
from config import db_name


class Database:
    '''
        \nUsers:
        \n* tg_id _int_\n* name _str_\n* santa _int_ \n  * value: tg_id получателя | 0\n

        \n
    '''
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
            self.GenerateTable(table_name='Users', tg_id="INTEGER", name="STRING", santa="INTEGER DEFAULT 0")


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


    def GetOne(self, data, table_name, find_param, find_value) -> list|bool:
        '''
        f'SELECT {data} FROM {table_name} WHERE {find_param} = {find_value}'
        
        - вернет первое найденное значение 
        '''
        try:
            query = f'SELECT {data} FROM {table_name} WHERE {find_param} = {find_value}'

            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connect.commit()

            if result == None:
                return False
            
            if data == '*':
                return result
            
            return result[0]
        
        except sqlite3.Error as e:
            print(f"[sql GetOne] {e}")
            return False


    def GetAll(self, data, table_name, find_param, find_value) -> list|bool:
        '''
        f'SELECT {data} FROM {table_name} WHERE {find_param} = {find_value}'
        
        - вернет список со всеми найденным значениями
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


    def Replace(self, table_name, row, new_value, find_param, find_value):
        '''
        UPDATE "{table_name}" SET {row} = ? WHERE {find_param} = ?;\n
        self.cursor.execute(command, (new_value, find_value))
        '''
        try:
            command = f'''
            UPDATE "{table_name}" 
            SET {row} = ? 
            WHERE {find_param} = ?;
            '''
            
            self.cursor.execute(command, (new_value, find_value))

            self.connect.commit()
            return True
        
        except Exception as e:
            print('[sql Replace]', e)
            return False
    
    
    def GetConnect(self):
        return self.connect


    def GetCursor(self):
        return self.cursor


