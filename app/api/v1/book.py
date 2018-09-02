from flask import jsonify

from sqlalchemy import or_
from app.models.book import Book
from app.validators.forms import BookSearchForm
from app.libs.redprint import Redprint
# book = Blueprint('book', __name__)
api = Redprint('book')


@api.route('/search')
def search():
    """
    书籍搜索, 
    """
    form = BookSearchForm().validate_for_api()
    q = '%' + form.q.data + '%'
    books = Book.query.filter(or_(Book.title.like(q), Book.publisher.like(q))).all()
    books = [book.hide('summary') for book in books]
    return jsonify(books)


@api.route('/<isbn>/detail')
def detail(isbn):
    books = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(books)
