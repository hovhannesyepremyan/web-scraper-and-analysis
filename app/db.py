import sqlite3


class DB:
    def __init__(self, database):
        self.database = database
        self._connection = None
        self._cursor = None

    @property
    def connection(self):
        if not self._connection:
            self._connection = sqlite3.connect(self.database)
        return self._connection

    @property
    def cursor(self):
        if not self._cursor:
            self._cursor = self.connection.cursor()
        return self._cursor

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS books (
            title TEXT,
            category TEXT,
            price FLOAT,
            rating INTEGER
        )
        """
        self.cursor.execute(query)

    def create(self, data):
        query = "INSERT INTO books (title, category, price, rating) VALUES(?, ?, ?, ?)"
        self._cursor.executemany(query, data)
        self._connection.commit()
        return self.cursor.rowcount

    def select(self, category: str=None):
        query = "SELECT * FROM books"
        params = ()
        if category:
            query += f" WHERE category = ?"
            params = (category,)
        data = self.cursor.execute(query, params).fetchall()
        return data

    def get_categories(self):
        query = "SELECT DISTINCT category FROM books ORDER BY category"
        cursor = self.cursor.execute(query)
        categories = [row[0] for row in cursor.fetchall()]
        return categories

    def is_empty(self):
        query = "SELECT count(*) FROM books"
        c = self.cursor.execute(query).fetchone()[0]
        return not bool(c)
