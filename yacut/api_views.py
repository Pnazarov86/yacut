from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import create_short_link


@app.route('/api/id/', methods=['POST'])
def create_link():
    """View-функция создания новой короткой ссылки."""
    return jsonify(create_short_link(request.get_json())), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Получение оригинальной ссылки по короткой ссылке."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(url=url_map.original), 200
