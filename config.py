import os
import logging

from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = 'my_books.db'

FLASK_HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
FLASK_PORT = os.environ.get('FLASK_PORT', 8000)
DEBUG = True

CATEGORIES = ('travel_2', 'mystery_3', 'historical-fiction_4', 'classics_6', 'womens-fiction_9', 'fiction_10', 'fantasy_19')

LOG_LEVEL = logging.INFO
if os.environ.get('FLASK_ENV') == 'development':
    LOG_LEVEL = logging.DEBUG
