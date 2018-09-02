from flask import g
from sqlalchemy import Column, String, Integer, orm

from apps.libs.error_code import Forbidden
from apps.models.base import Base, db


class Article(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    content = Column(String(140))
    author = Column(Integer, default=1)

    def keys(self):
        return ['id', 'title', 'content']

    def __getitem__(self, item):
        return getattr(self, item)

    def delete(self):
        self.is_own_article()
        with db.auto_commit():
            db.session.delete(self)

    def is_own_article(self):
        if g.user.id == self.author or g.user.scope == 'AdminScope':
            return True
        else:
            raise Forbidden()




