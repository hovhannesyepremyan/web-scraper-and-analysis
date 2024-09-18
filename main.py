from flask import Flask

from app.db import DB
from app.views import book
from app.helper import Parser


app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)

app.logger.setLevel(app.config['LOG_LEVEL'])

book_prefix = '/'

app.register_blueprint(book, url_prefix=book_prefix)

app.logger.info('Application Started Successfully')

db = DB(database='my_books.db')
db.create_table()
if db.is_empty():
    for category in app.config['CATEGORIES']:
        parser = Parser(category=category)
        parser.fetch_data()
        count = db.create(parser.books)
        app.logger.info(f"{count} rows inserted.")


if __name__ == '__main__':
    app.run(host=app.config['FLASK_HOST'],
            port=app.config['FLASK_PORT'],
            debug=app.config['DEBUG'])
