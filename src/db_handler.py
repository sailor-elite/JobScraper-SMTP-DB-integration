from db_init import Database
import sqlite3



class DataHandler():

    def __init__(self,db_file):
        self.db = Database(db_file)
        self.conn = self.db.conn

    def insert_data(self, data):

        name, date, job = data

        sql = '''SELECT * FROM projects WHERE name = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (name,))
        existing_record = cur.fetchone()

        if existing_record:

            existing_date = existing_record[2]
            if date > existing_date:
                sql = '''UPDATE projects SET date = ? WHERE name = ?'''
                cur.execute(sql, (date, name))
                self.conn.commit()
                print(f"updated job's {name} date with {date}")
            else:
                print(f"Job {name} exists with the same or different date.")
        else:
            sql = ''' INSERT INTO projects(name, date, job)
                      VALUES(?,?,?) '''
            cur.execute(sql, data)
            self.conn.commit()
            print(f"added new job: {name}")

