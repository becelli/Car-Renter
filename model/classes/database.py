import sqlite3
class database:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.db = sqlite3.connect('../database/database.db')
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()

    def execute(self, query, data=None):
        self.cursor.execute(query, data)
        self.db.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()