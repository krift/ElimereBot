import psycopg2
import os
import logging, logging.config
from configparser import ConfigParser
from psycopg2 import pool

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:

    def __init__(self):
        self.conn_pool = self.create_connection_pool()

    def log_error(self, e, function_called):
        """
        This function logs errors to info.log in the main directory.
        :param e: The error
        :param function_called: The function that the error was produced in
        :return:
        """
        logger = logging.getLogger(f"discordBot.Logging.Database.{function_called}")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(f"{PATH}/info.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.error("-------------------------")
        logger.error(e)

    def config(self, filename=f"{PATH}/config.ini", section="postgresql"):
        """
        Simple config parser to load database connection info
        :param filename: The name of the file to load
        :param section: The section of the file to load
        :return: Returns a dictionary of database connection info
        """
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f"Section{section} not found in the {filename} file")
        return db

    def create_connection_pool(self):
        """
        This creates a connection pool for the database.
        :return: Returns a pool of connections
        """
        conn_pool = None
        try:
            params = self.config()
            conn_pool = psycopg2.pool.SimpleConnectionPool(5, 10, **params)
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(f'Error in config file: {error}', 'create_connection_pool')
        return conn_pool

    def retrieve_connection(self):
        """
        Retrieve a single connection from the connection pool.
        :return: DB Connection
        """
        if self.conn_pool:
            return self.conn_pool.getconn()

    def return_connection(self, conn):
        """
        Returns a single connection back to the connection pool.
        :param conn: A database connection
        :return:
        """
        self.conn_pool.putconn(conn)

    def close_conn_pool(self):
        """
        This closes all connections to the database.
        :return:
        """
        if self.conn_pool:
            self.conn_pool.closeall()

    def create_tables(self):
        """
        This runs on bot startup. Will create the correct tables if they don't already exist.
        """
        commands = (
            """
        CREATE TABLE IF NOT EXISTS logs (
        log_id TEXT PRIMARY KEY UNIQUE,
        log_date TEXT NOT NULL,
        log_title TEXT NOT NULL,
        log_zone INTEGER NOT NULL
        )
        """,
            """
            CREATE TABLE IF NOT EXISTS tags (
            tag_label TEXT PRIMARY KEY UNIQUE,
            tag_author TEXT NOT NULL,
            tag_text TEXT
            )
        """,
            """
            CREATE TABLE IF NOT EXISTS wowhead (
            wowhead_date TEXT PRIMARY KEY,
            date TEXT
            )
        """,
            """
            CREATE TABLE IF NOT EXISTS discordroles (
            id SERIAL PRIMARY KEY,
            server_id TEXT,
            guild_name TEXT,
            roles_assign TEXT [],
            report_channel TEXT NULL,
            roles_channel TEXT NULL
            )
        """,
        )
        conn = None
        try:
            # read the connection parameters
            # connect to the PostgreSQL server
            conn = self.retrieve_connection()
            cur = conn.cursor()
            # create table one by one
            for command in commands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError)as e:
            self.log_error(e, 'create_tables')
        finally:
            if conn is not None:
                self.return_connection(conn)

    def check_table(self, table_name):
        """
        This checks a specific table for any data and returns one single piece of data
        :param table_name: The name of the table to check
        :return:
        """
        sql = f"""SELECT * FROM {table_name} LIMIT 1"""
        conn = None
        row_found = []
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql,)
            row_found = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'check_table')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found

    async def insert_log_data(self, log_id, log_date, log_title, log_zone):
        """
        This inserts a log into the logs table
        :param log_id: The ID of the log
        :param log_date: The date of the log
        :param log_title: The title of the log
        :param log_zone: The zone of the log
        :return: Returns the number of rows inserted, should be 1
        """
        sql = """INSERT INTO logs(log_id, log_date, log_title, log_zone) VALUES (%s, %s, %s, %s)"""
        conn = None
        inserted_rows = None
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (log_id, log_date, log_title, log_zone))
            inserted_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'insert_log_data')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return inserted_rows

    async def read_log_table(self, log_id):
        """
        This reads the log table looking for a specific log with a specific ID
        :param log_id: The ID of the log
        :return: Returns how many rows it found, between 0 and 1
        """
        sql = """SELECT log_id FROM logs WHERE log_id = %s"""
        conn = None
        row_found = ''
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (log_id, ))
            row_found = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'read_log_table')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found

    async def select_log_by_date(self, log_date):
        """
        Selects all logs according to it's recorded date
        :param log_date: The date of the log
        :return: Returns the data from the logs database if found, else None
        """
        sql = """SELECT log_id, log_title FROM logs WHERE log_date = %s"""
        conn = None
        row_found = ''
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (log_date,))
            row_found = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'select_log_by_date')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found

    async def select_log_by_zone(self, log_zone):
        """
        Selects all logs according to it's recorded zone
        :param log_zone: The zone entered, must be an integer
        :return: Returns all logs found or None
        """
        sql = """SELECT log_id, log_date, log_title FROM logs WHERE log_zone = %s"""
        conn = None
        logs_found = []
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (log_zone,))
            logs_found = cur.fetchall()
            print(logs_found)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'select_log_by_zone')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return logs_found

    async def insert_tag_data(self, tag_label, tag_author, tag_text):
        """
        Inserts a tag into the tags database with the specified information
        :param tag_label: The tags label
        :param tag_author: The author of the tag
        :param tag_text: The actual text of the tag
        :return: Returns the number of rows inserted, between 0 and 1
        """
        sql = """INSERT INTO tags(tag_label, tag_author, tag_text) VALUES (%s, %s, %s)"""
        conn = None
        inserted_rows = None
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (tag_label, tag_author, tag_text))
            inserted_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'insert_tag')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return inserted_rows

    async def update_tag_data(self, tag_label, tag_text):
        """
        Updates a specific tag in the tags table
        :param tag_label: The tags label
        :param tag_text: The new text
        :return: Returns the number of rows updated, between 0 and 1
        """
        sql = """UPDATE tags SET tag_text = %s WHERE tag_label = %s"""
        conn = None
        updated_rows = None
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (tag_text, tag_label))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'update_tag')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return updated_rows

    async def select_tag_data(self, tag_label):
        """
        Selects a specific tag with a specific label
        :param tag_label: The label to select
        :return: Returns either the found row or None
        """
        sql = """SELECT tag_text, tag_author FROM tags WHERE  tag_label = %s"""
        conn = None
        found_row = None
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (tag_label,))
            found_row = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'select_tag')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return found_row

    async def delete_tag_data(self, tag_label):
        """
        Deletes a specific tag with a specific label
        :param tag_label: The label to delete
        :return: Returns the number of rows deleted, between 0 and 1
        """
        sql = """DELETE FROM tags WHERE tag_label = %s"""
        conn = None
        deleted_rows = None
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (tag_label, ))
            deleted_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'delete_tag')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return deleted_rows

    async def select_all_tag_data(self, tag_author):
        """
        This selects all tag data from a specific author
        :param tag_author: The author to search for
        :return: Returns all related tags from that author
        """
        sql = """SELECT tag_label, tag_text FROM tags WHERE tag_author = %s"""
        conn = None
        selected_rows = []
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (tag_author, ))
            selected_rows = cur.fetchall()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'select_all_tag')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return selected_rows

    async def insert_wowhead_date(self, date):  # These wowhead database commands will likely in the future.
        """
        Inserts a date into the wowhead table
        :param date: The date to enter
        :return:
        """
        sql = """INSERT INTO wowhead( wowhead_date, date) VALUES (%s, %s)"""
        conn = None
        inserted_rows = None
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, ("wowhead_date", date))
            inserted_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'insert_wowhead')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return inserted_rows

    async def update_wowhead_date(self, date):
        """
        Updates the date in the wowhead table
        :param date: The new date
        :return:
        """
        sql = """UPDATE wowhead SET date = %s WHERE wowhead_date = %s"""
        conn = None
        updated_rows = None
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (date, 'wowhead_date'))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'update_wowhead')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return updated_rows

    async def select_wowhead_date(self):
        """
        This selects the date from the wowhead table
        :return:
        """
        sql = """SELECT date FROM wowhead WHERE wowhead_date = %s"""
        conn = None
        row_found = ''
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, ('wowhead_date', ))
            row_found = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'select_wowhead')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found

    async def insert_discordroles_data(self, server_id, guild_name, roles_assign, report_channel, roles_channel):
        """
        This inserts a string representation of the name of a role on a discord server to be used with permissions
        :param server_id: The server's ID
        :param guild_name: The name of the guild
        :param roles_assign: The roles to assign
        :param report_channel: The channel to report in
        :param roles_channel: The actual roles channel
        :return:
        """
        sql = """INSERT INTO discordroles (server_id, guild_name, roles_assign, report_channel, roles_channel)
        VALUES (%s, %s, %s, %s, %s, %s)"""
        conn = None
        inserted_rows = None
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (server_id, guild_name, roles_assign, report_channel, roles_channel))
            inserted_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'insert_discordroles')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return inserted_rows

    # async def update_discordroles_data(self):

    # async def delete_discordroles_data(self, server_id, role_type):

    async def select_discordroles_data(self, server_id):
        """
        Selects the discord roles data from the table
        :param server_id: The server ID
        :return:
        """
        sql = """SELECT * FROM discordroles WHERE server_id = %s"""
        conn = None
        row_found = ''
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, server_id)
            row_found = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error, 'select_discordroles')
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found
