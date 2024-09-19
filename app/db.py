import sqlite3


class DB:
    _CONNECTION = None
    _CURSOR = None
    SELECT_ALL_QUERY = "SELECT * FROM books"

    @classmethod
    def set_connection(cls, database):
        cls._CONNECTION = sqlite3.connect(database, check_same_thread=False)

    @classmethod
    def set_cursor(cls):
        cls._CURSOR = cls._CONNECTION.cursor()

    @classmethod
    def get_connection(cls):
        return cls._CONNECTION

    @classmethod
    def create_table(cls):
        query = """
        CREATE TABLE IF NOT EXISTS books (
            title TEXT,
            category TEXT,
            price FLOAT,
            rating INTEGER
        )
        """
        cls._CURSOR.execute(query)

    @classmethod
    def create(cls, data):
        query = "INSERT INTO books (title, category, price, rating) VALUES(?, ?, ?, ?)"
        cls._CURSOR.executemany(query, data)
        cls._CONNECTION.commit()
        return cls._CURSOR.rowcount

    @classmethod
    def select(cls, category: str=None):
        query = cls.SELECT_ALL_QUERY
        params = ()
        if category:
            query += " WHERE category = ?"
            params = (category,)
        data = cls._CURSOR.execute(query, params).fetchall()
        return data

    @classmethod
    def get_categories(cls):
        query = "SELECT DISTINCT category FROM books ORDER BY category"
        cursor = cls._CURSOR.execute(query)
        categories = [row[0] for row in cursor.fetchall()]
        return categories

    @classmethod
    def is_empty(cls):
        query = "SELECT count(*) FROM books"
        count = cls._CURSOR.execute(query).fetchone()[0]
        return count == 0
