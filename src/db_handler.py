from db_init import Database
import sqlite3

from datetime import datetime

def convert_date_to_sql_format(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")

class DataHandler():

    def __init__(self,db_file):
        self.db = Database(db_file)
        self.conn = self.db.conn

    def insert_data(self, data):
        name, date, location, job  = data
        date = convert_date_to_sql_format(date)
        sql = '''SELECT * FROM projects WHERE name = ? AND job = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (name, location))
        existing_record = cur.fetchone()

        if existing_record:
            existing_date = existing_record[2]
            if date > existing_date:
                sql = '''UPDATE projects SET date = ? WHERE name = ? AND job = ?'''
                cur.execute(sql, (name, date, location, job))
                self.conn.commit()
                print(f"Updated job '{name}' in location '{location}' with new date {date}")
            else:
                print(f"Job '{name}' in location '{location}' exists with the same or newer date.")
        else:
            sql = '''INSERT INTO projects(name, date, location, job)
                     VALUES(?,?,?,?)'''
            cur.execute(sql, (name, date, location,job))
            self.conn.commit()
            print(f"Added new job: '{name}' in location '{job}'")


