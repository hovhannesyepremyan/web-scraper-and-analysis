import sqlite3

class DB:
    def __init__(self, database_name):
        self.database_name = database_name
        self._connection = None
        self._cursor = None

    @property
    def connection(self):
        if not self._connection:
            self._connection = sqlite3.connect(self.database_name)
        return self._connection

    @property
    def cursor(self):
        if not self._cursor:
            self._cursor = self.connection.cursor()
        return self._cursor

    def create_table(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS books (
            title TEXT,
            category TEXT,
            price FLOAT,
            rating INTEGER
        )
        """
        self.cursor.execute(create_statement)

    def save(self, data):
        insert_statement = "INSERT INTO books (title, category, price, rating) VALUES(?, ?, ?, ?)"
        try:
            self._cursor.executemany(insert_statement, data)
            self._connection.commit()
            print(f"{self.cursor.rowcount} rows inserted.")
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
        finally:
            self._cursor.close()
            self._cursor = None

    def select(self, category: str=None):
        select_statement = "SELECT * FROM books"
        if category:
            select_statement += f"WHERE category={category}"
        data = self.cursor.execute(select_statement).fetchall()
        self._cursor.close()
        self._cursor = None
        return data


