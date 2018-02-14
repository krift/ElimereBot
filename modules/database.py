import sqlite3
import asyncio


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data/elidb')
        self.create_table()

    async def close(self):
        self.conn.close()

    async def create_table(self):  # TODO: Add name parameter
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS storage(label TEXT PRIMARY KEY unique, msg TEXT)''')
        self.conn.commit()

    async def insert_data(self, label, msg):  # TODO: Add data parameters
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO storage(label, msg) VALUES(?,?)''',
                           (label, msg))
            self.conn.commit()
            return 'Stored'
        except sqlite3.IntegrityError:
            return 'A message with this label already exists.'

    async def retrieve_data(self, label):  # TODO: Add parameters
        cursor = self.conn.cursor()
        cursor.execute('''SELECT msg FROM storage WHERE label = ?''', (label,))
        msg = cursor.fetchone()
        if msg is None:
            return 'Nothing found with the label' + label
        else:
            return msg

    async def update_data(self, label, msg):  # TODO: Add parameters
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE storage SET msg = ? WHERE label = ?''', (msg, label))
        self.conn.commit()

    async def delete_data(self, label):  # TODO: Add Parameters
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM storage WHERE label = ?''', (label,))
        self.conn.commit()
