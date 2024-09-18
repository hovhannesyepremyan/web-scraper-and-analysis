from flask import Blueprint, request, render_template
import pandas as pd

from .db import DB
from config import DATABASE_NAME

book = Blueprint('books', __name__)


@book.route('/', methods=['GET'])
def books_list():
    db = DB(database=DATABASE_NAME)

    category = request.args.get('category', None)
    books = db.select(category=category)
    categories = db.get_categories()

    return render_template('books.html', books=books, categories=categories, current_category=category)


@book.route('/analytics')
def analytics():
    db = DB(database=DATABASE_NAME)
    df = pd.read_sql_query("SELECT * FROM books", db.connection)
    db._connection.close()

    stats = df.describe().round(2)
    stats_dict = stats.to_dict()

    books_per_category = df['category'].value_counts().to_dict()

    return render_template('analytics.html', stats=stats_dict, books_per_category=books_per_category)
