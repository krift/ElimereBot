import psycopg2
import os
import logging, logging.config
from configparser import ConfigParser
from psycopg2 import pool

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:

    def __init__(self):
        self.conn_pool = self.create_connection_pool()

    def log_error(self, e):
        logger = logging.getLogger("discordBot.Logging")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(f"{PATH}/info.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.error("-------------------------")
        logger.error(e)

    def config(self, filename=f"{PATH}/config.ini", section="postgresql"):
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
        conn_pool = None
        try:
            params = self.config()
            conn_pool = psycopg2.pool.SimpleConnectionPool(5, 10, **params)
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(f'Error in config file: {error}')
        return conn_pool

    def retrieve_connection(self):
        if self.conn_pool:
            return self.conn_pool.getconn()

    def return_connection(self, conn):
        self.conn_pool.putconn(conn)

    def close_conn_pool(self):
        if self.conn_pool:
            self.conn_pool.closeall()

    def create_tables(self):
        """This runs on bot startup. Will create the correct tables if they don't already exist."""
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
            """
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
            self.log_error(e)
        finally:
            if conn is not None:
                self.return_connection(conn)

    def check_table(self, table_name):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found

    async def insert_log_data(self, log_id, log_date, log_title, log_zone):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return inserted_rows

    async def read_log_table(self, log_id):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found

    async def select_log_by_date(self, log_date):
        sql = """SELECT log_id, log_title FROM logs WHERE log_date = %s"""
        conn = None
        row_found = ''
        try:
            conn = self.retrieve_connection()
            cur = conn.cursor()
            cur.execute(sql, (log_date,))
            row_found = cur.fetchone()
            print(row_found)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found

    async def select_log_by_zone(self, log_zone):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return logs_found

    async def insert_tag_data(self, tag_label, tag_author, tag_text):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return inserted_rows

    async def update_tag_data(self, tag_label, tag_text):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return updated_rows

    async def select_tag_data(self, tag_label):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return found_row

    async def delete_tag_data(self, tag_label):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return deleted_rows

    async def select_all_tag_data(self, tag_author):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return selected_rows

    async def insert_wowhead_date(self, date):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return inserted_rows

    async def update_wowhead_date(self, date):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return updated_rows

    async def select_wowhead_date(self):
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
            self.log_error(error)
        finally:
            if conn is not None:
                self.return_connection(conn)
        return row_found
