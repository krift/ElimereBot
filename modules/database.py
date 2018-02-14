import sqlite3
import os
import asyncio
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(PATH+'/data/elidb')
        self.create_table()

    async def close(self):
        self.conn.close()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS storage(label TEXT PRIMARY KEY unique, author TEXT, msg TEXT)''')
        self.conn.commit()

    async def insert_data(self, label, author, msg):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO storage(label,author, msg) VALUES(?,?,?)''',
                           (label, author, msg))
            self.conn.commit()
            return 'Stored'
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return 'A message with this label already exists.'

    async def retrieve_data(self, label):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT msg, author FROM storage WHERE label = ?''', (label,))
        msg = cursor.fetchone()
        if msg is None:
            return 'Nothing found with the label ' + label
        else:
            return " ".join(msg)

    async def retrieve_all_labels(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT label, author FROM storage''')
        data = cursor.fetchall()
        if not data:
            return "There are no messages stored.", False
        else:
            return data, True

    async def update_data(self, label, msg):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE storage SET msg = ? WHERE label = ?''', (msg, label))
        self.conn.commit()

    async def delete_data(self, label):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM storage WHERE label = ?''', (label,))
        self.conn.commit()

    async def create_new_table(self, drop_table, new_table):
        cursor = self.conn.cursor()
        cursor.execute(f'''DROP TABLE IF EXISTS {drop_table}''')
        self.conn.commit()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {new_table}(label TEXT PRIMARY KEY unique, author TEXT, msg TEXT)''')
        self.conn.commit()
