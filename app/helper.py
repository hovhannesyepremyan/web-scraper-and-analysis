import requests
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, category, storage=None):
        self.storage = storage
        self._url = "http://books.toscrape.com/catalogue/category/books/{0}/index.html"
        self._category = category
        self._response = None
        self._soup = None
        self.books = []

    @property
    def url(self):
        return self._url.format(self._category)

    @property
    def response(self):
        if self._response is None:
            self._response = requests.get(self.url)
        return self._response

    @property
    def soup(self):
        if self._soup is None and self.response:
            self._soup = BeautifulSoup(self.response.text, 'html.parser')
        return self._soup

    @property
    def category(self):
        self._category = self._soup.find('h1').text
        return self._category

    def fetch_data(self):
        if self.check_status():
            self.soup()
            self.parse_books()
        else:
            pass
            # TODO: log
            # print(f"Failed to retrieve the page. Status code: {self._response.status_code}")

    def check_status(self):
        return self.response.status_code == 200

    def get_books(self):
        return self._soup.find_all('article', class_='product_pod')

    def parse_books(self):
        for book in self.get_books():
            title, price, rating = self.parse_book_data(book)
            self.books.append((title, self.category, float(price), rating))

    def parse_book_data(self, book):
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_='price_color').text[2:]
        rating_class = book.find('p', class_='star-rating')['class'][1]
        ratings = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = ratings.get(rating_class, 0)
        return title, price, rating
