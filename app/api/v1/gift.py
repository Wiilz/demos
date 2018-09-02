from flask import g
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.gift import Gift
from app.libs.error_code import Success, DumplicatedGift
api = Redprint('gift')



@api.route('/isbn', methods=['POST'])
@auth.login_required
def create(isbn):
    uid = g.user.uid
    with db.auto_commit():
        book = Book.query.filter_by(isbn=isbn).first_or_404()
        gift = Gift.query.filter_by(isbn=isbn, uid=uid).first()
        if gift:
            raise DumplicatedGift()
        gift = Gift()
        gift.uid = uid
        gift.isbn = isbn
        db.session.add(gift)
    return Success()
