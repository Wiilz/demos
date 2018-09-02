import ipdb
from flask import Blueprint, request, render_template, jsonify, redirect
from apps.model import Url
from apps.validates.url import UrlForm
urlbp = Blueprint('uri', __name__)


@urlbp.route('/api/short', methods=['POST'])
def api():
    form = UrlForm().validate_for_api()
    url = Url.save_url(form.long_url.data)
    return jsonify({'url': url.short_url}), 200


@urlbp.route('/<code>')
def redirect_to_long(code):
    long_url = Url.convert_to_long()
    return redirect(long_url, code=301)


@urlbp.route('/')
def index():
    return render_template('index.html')

