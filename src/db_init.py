import sqlite3

from _sqlite3 import Error

import sqlite3

from _sqlite3 import Error

class Database:

    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.db_file = db_file

    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self, create_table_sql):

        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)








