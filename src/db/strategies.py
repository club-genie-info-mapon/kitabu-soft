import sqlite3

try:
    import pymysql
except ImportError:
    pymysql = None

class DatabaseStrategy:
    """
    Abstract base class for database strategies.
    """
    def connect(self):
        raise NotImplementedError

    def execute(self, query, params=None):
        raise NotImplementedError

    def fetchall(self):
        raise NotImplementedError

    def fetchone(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

class SQLiteStrategy(DatabaseStrategy):
    """
    SQLite implementation of the database strategy.
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.type = "sqlite"

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

class MySQLStrategy(DatabaseStrategy):
    """
    MySQL implementation of the database strategy using PyMySQL.
    """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.type = "mysql"

    def connect(self):
        if pymysql is None:
            raise ImportError("pymysql is not installed.")
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.Cursor
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
