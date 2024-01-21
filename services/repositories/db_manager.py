import sqlite3
from flask import current_app

from utils.singleton import Singleton


class DbManager(Singleton):
    def __init__(self):
        self.clear = False
        self.db = None
        self.cursor = None

    def connect(self):
        self.clear = current_app.config["CLEAR_DB"]
        self.db = sqlite3.connect(current_app.config["DATABASE"])
        self.cursor = self.db.cursor()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.lastrowid

    def fast_exec(self, query, params=()):
        self.connect()
        exec_id = self.execute(query, params)
        row = self.cursor.fetchall()
        self.commit()
        self.close()
        return row

    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()

    def should_clear_db(self):
        self.clear

    def clear_table_if_should(self, table_name):
        if self.clear:
            self.connect()
            self.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.execute(f"DELETE FROM {table_name}")
            self.commit()
            self.close()
