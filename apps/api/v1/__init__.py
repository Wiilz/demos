from flask import Blueprint
from apps.api.v1 import user, article


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__, url_prefix='/v1')
    bp_v1.add_url_rule('/user', view_func=user.UserResource.as_view('user'))
    bp_v1.add_url_rule('/auth', view_func=user.AuthResource.as_view('auth'))
    bp_v1.add_url_rule('/article', view_func=article.ArticleResource.as_view('article'))
    bp_v1.add_url_rule('/article/<int:id>', view_func=article.ArticleSigleResource.as_view('articlesigle'))
    return bp_v1
