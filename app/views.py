from flask import Blueprint, request, render_template
import pandas as pd

from .db import DB


book = Blueprint('books', __name__)


@book.route('/', methods=['GET'])
def books_list():
    category = request.args.get('category', None)
    books = DB.select(category=category)
    categories = DB.get_categories()

    return render_template('books.html', books=books, categories=categories, current_category=category)


@book.route('/analytics')
def analytics():
    df = pd.read_sql_query(DB.SELECT_ALL_QUERY, DB.get_connection())

    stats = df.describe().round(2)
    stats_dict = stats.to_dict()

    books_per_category = df['category'].value_counts().to_dict()

    return render_template('analytics.html', stats=stats_dict, books_per_category=books_per_category)
