from datetime import datetime
from flask import current_app, request
from apps.ext import db
from apps.libs.code import generic_codes
from apps.libs.error import ApiException


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url_code = db.Column(db.String(32))
    long_url = db.Column(db.String(1000))
    create_time = db.Column(db.DateTime(), default=datetime.now)

    @classmethod
    def is_unique_short_url(cls, value=None):
        """ 传入code判断是否唯一"""
        urls = cls.query.filter_by(short_url_code=value).first()
        if urls:
            return False
        else:
            return True

    @property
    def short_url(self):
        """短域名"""
        return current_app.config['BASE_URL'] + self.short_url_code

    @classmethod
    def generic_short_url_code(cls):
        short_url_code = generic_codes(5)
        return short_url_code if cls.is_unique_short_url(short_url_code) else generic_short_url_code(cls)
    
    @classmethod
    def save_url(cls, long_url):
        url = cls.has_the_long_url(long_url)
        if url:
            return url
        short_url_code = cls.generic_short_url_code() 
        url = cls(short_url_code=short_url_code, long_url=long_url)
        db.session.add(url)
        db.session.commit()
        return url

    @classmethod
    def has_the_long_url(cls, long_url):
        url = cls.query.filter_by(long_url=long_url).first()
        return url if url else None

    @classmethod
    def convert_to_long(cls):
        """短域名访问后需要转为常常的域名"""
        code = request.path.strip('/')
        url = cls.query.filter_by(short_url_code=code).first()
        if url:
            long_url = url.long_url
            if not long_url.startswith('http'):
                long_url = 'http://' + long_url 
            return long_url
        else:
            raise ApiException(msg='not found', code=404, error_code=404)
            
