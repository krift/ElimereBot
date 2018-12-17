import sqlite3
import os
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(PATH+'/data/elidb')  # Connect to the database

    async def close(self):
        """This closes the connection with the database"""
        self.conn.close()

    def create_table(self, db_string):
        """This will create a table if one doesn't already exist"""
        cursor = self.conn.cursor()  # Create a cursor object
        cursor.execute(db_string)
        self.conn.commit()  # Commit changes to the database table

    async def insert_data(self, db_string, data):
        try:
            cursor = self.conn.cursor()
            cursor.execute(db_string, data)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()

    async def read_table(self, db_string, data, select_all=False):
        cursor = self.conn.cursor()
        if data is '':
            cursor.execute(db_string)
        else:
            cursor.execute(db_string, [data])
        if select_all is True:
            data = cursor.fetchall()
        else:
            data = cursor.fetchone()
        if not data:
            return False
        else:
            return True

    async def pull_data(self, db_string, data, select_all=False):
        """Pull specific data from the table"""
        cursor = self.conn.cursor()  # Create a cursor object
        if data == '':
            if select_all is True:
                value = cursor.execute(db_string).fetchall()
            else:
                value = cursor.execute(db_string).fetchone()
        elif isinstance(data, list) is False and isinstance(data, tuple) is False:
            if select_all is True:
                value = cursor.execute(db_string, (data,)).fetchall()
            else:
                value = cursor.execute(db_string, (data,)).fetchone()
        else:
            if select_all is True:
                value = cursor.execute(db_string, data).fetchall()
            else:
                value = cursor.execute(db_string, data).fetchone()
        if value is None:
            return None
        else:
            return value

    async def update_data(self, db_string, data):
        try:
            cursor = self.conn.cursor()  # Create the cursor object
            cursor.execute(db_string, data)  # Update the row
            self.conn.commit()  # Commit the changes
        except sqlite3.IntegrityError:
            self.conn.rollback()

    async def delete_data(self, db_string, data):
        try:
            cursor = self.conn.cursor()
            if isinstance(data, list) is False and isinstance(data, tuple) is False:
                cursor.execute(db_string, (data,))
            else:
                cursor.execute(db_string, data)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()
