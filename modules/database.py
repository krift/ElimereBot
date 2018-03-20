import sqlite3
import os
import datetime
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(PATH+'/data/elidb')  # Connect to the database
        self.create_table()  # Call the create_table function

    async def close(self):
        """This closes the connection with the database"""
        self.conn.close()

    def create_table(self):
        """This will create a table if one doesn't already exist"""
        cursor = self.conn.cursor()  # Create a cursor object
        cursor.execute('''CREATE TABLE IF NOT EXISTS storage(label TEXT PRIMARY KEY unique, author TEXT, msg TEXT)''')  # Create the table
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (id TEXT PRIMARY KEY unique, date TEXT, title TEXT, zone TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS errors (id INTEGER PRIMARY KEY autoincrement, date TEXT, server TEXT, command TEXT, error TEXT)''')
        self.conn.commit()  # Commit changes to the database table

    async def insert_tag_data(self, *data):
        """Inserts specific data into the database table"""
        try:
            cursor = self.conn.cursor()  # Create a cursor object
            cursor.execute('''INSERT INTO storage(label,author, msg) VALUES(?,?,?)''',
                           data)  # Insert the data into the table
            self.conn.commit()  # Commit changes
            return 'Stored'  # Return a string
        except sqlite3.IntegrityError:  # If the table already contains this specific label
            self.conn.rollback()  # Rollback changes
            return 'A message with this label already exists.'  # Return a string

    async def retrieve_data(self, label):
        """This pulls a specific row from the table"""
        cursor = self.conn.cursor()  # Create a cursor object
        cursor.execute('''SELECT msg, author FROM storage WHERE label = ?''', (label,))  # Select the row
        msg = cursor.fetchone()  # Fecth the information
        if msg is None:  # If the data doesn't exist in the table
            return 'Nothing found with the label ' + label  # Return a string
        else:
            return msg  # Return the data

    async def retrieve_all_labels(self):
        """This pulls all rows from the table"""
        cursor = self.conn.cursor()  # Create the cursor object
        cursor.execute('''SELECT label, author FROM storage''')  # Select all rows
        data = cursor.fetchall()  # Fetch all rows
        if not data:
            return "There are no messages stored.", False   # If there are no rows in the table
        else:
            return data, True  # Return the data

    async def update_data(self, label, msg):
        """Update a specific row in the table"""
        cursor = self.conn.cursor()  # Create the cursor object
        cursor.execute('''UPDATE storage SET msg = ? WHERE label = ?''', (msg, label))  # Update the row
        self.conn.commit()  # Commit the changes

    async def delete_data(self, label):
        """Deletes a specific row from the table"""
        cursor = self.conn.cursor()  # Create the cursor object
        cursor.execute('''DELETE FROM storage WHERE label = ?''', (label,))  # Select the row to delete and delete it
        self.conn.commit()  # Commit the changes

    async def insert_log_data(self, *data):
        """Inserts warcraft log data into the database table"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO logs (id, date, title, zone) VALUES(?,?,?,?)''', data)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()

    async def pull_log_by_date(self, date):
        """Pull logs by date"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id, title FROM logs where date = ?''', (date,))
        data = cursor.fetchall()
        print(data)
        if not data:
            return None
        else:
            return data

    async def check_log_by_id(self, id):
        """Querys the database for a specific id"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id FROM logs where id = ?''', (str(id),))
        data = cursor.fetchone()
        if not data:
            return False
        else:
            return True

    async def insert_error_data(self, *data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO errors (date, server, command, error) VALUES(?,?,?,?)''', (str(data[0]), str(data[1]), str(data[2]), str(data[3]),))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()

    async def create_new_table(self, table, table_data):
        """Drops the specified table and creates a new table with a specific name"""
        data = ''
        for string in table_data:
            data += string+" "
        cursor = self.conn.cursor()  # Create the cursor object
        cursor.execute(f'''DROP TABLE IF EXISTS {table}''')  # Drop the table
        self.conn.commit()  # Commit changes just in case
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table}({data})''')  # Create a new table
        self.conn.commit()  # Commit changes
