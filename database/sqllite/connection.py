from sqlite3 import connect

class SQLlite:
    def __init__(self) -> None:
        self.connection = connect('database/sqllite/sqlite.db')
