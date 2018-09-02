from flask import g

from flask import jsonify

from apps.libs.baseresoruce import BaseResource
from apps.libs.error_code import MethodNotAllowed, Success, GetListSuccess, DeleteSuccess
from apps.models.article import Article
from apps.models.base import db
from apps.validators.forms import ArticleForm
from apps.libs.token_auth import auth


class ArticleResource(BaseResource):
    """
    get: 获取所有文章
    post：添加文章
    """
    @auth.login_required
    def post(self):
        form = ArticleForm().validate_for_api()
        with db.auto_commit():
            article = Article()
            article.title = form.title.data
            article.content = form.content.data
            article.author = g.user.id
            db.session.add(article)
        return Success(msg=dict(article), code=201, error_code=1)

    def get(self):
        articles = Article.query.all()
        return GetListSuccess(msg=articles)


class ArticleSigleResource(BaseResource):
    """
    delete: 删除文章
    put： 修改文章
    """
    @auth.login_required
    def delete(self, id):
        aricle = Article.query.filter_by(id=id).first_or_404()
        aricle.delete()
        return DeleteSuccess()

    @auth.login_required
    def put(self):
        form = ArticleForm().validate_for_api()
        article = Article.query.filter_by(id=id).first_or_404()
        article.is_own_article()
        with db.auto_commit():
            article.title = form.title.data
            article.content = form.content.data
            db.session.add(article)
        return Success(msg=dict(article), code=201, error_code=1)
