from flask import request

from . import app
from .utils import create_short_link, get_original_url


@app.route('/api/id/', methods=['POST'])
def create_link():
    """View-функция создания новой короткой ссылки."""
    data = request.get_json()
    return create_short_link(data)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_link(short_id):
    """View-функция получение оригинальной ссылки по короткой ссылке."""
    return get_original_url(short_id)
