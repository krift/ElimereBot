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

    async def read_table(self, db_string, data):
        cursor = self.conn.cursor()
        if data is '':
            cursor.execute(db_string)
        else:
            cursor.execute(db_string, [data])
        data = cursor.fetchone()
        if not data:
            return False
        else:
            return True

    async def pull_data(self, db_string, data):
        """Pull specific data from the table"""
        cursor = self.conn.cursor()  # Create a cursor object
        cursor.execute(db_string, (data,))  # Select the row
        value = cursor.fetchone()  # Fecth the information
        if value is None:  # If the data doesn't exist in the table
            return False
        else:
            return value  # Return the data

    async def update_data(self, db_string, data):
        cursor = self.conn.cursor()  # Create the cursor object
        cursor.execute(db_string, data)  # Update the row
        self.conn.commit()  # Commit the changes

# TODO: Everything below here will be removed
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

    async def delete_data(self, label):
        """Deletes a specific row from the table"""
        cursor = self.conn.cursor()  # Create the cursor object
        cursor.execute('''DELETE FROM storage WHERE label = ?''', (label,))  # Select the row to delete and delete it
        self.conn.commit()  # Commit the changes

    async def pull_log_by_date(self, date):
        """Pull logs by date"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id, title FROM logs where date = ?''', (date,))
        data = cursor.fetchall()
        if not data:
            return None
        else:
            return data

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
