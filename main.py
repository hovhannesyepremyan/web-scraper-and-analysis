from db import DB
from helper import Parser


parser = Parser(category="historical-fiction_4")
# parser1 = Parser(category="historical-fiction_4")

parser.fetch_data()
data = parser.books
# print(data)
# parser1.fetch_data()
# print(parser.books[3])
# print(parser1.category, parser1.books)

db = DB(database_name='my_books.db')
db.create_table()
db.save(data)
print(db.select())


