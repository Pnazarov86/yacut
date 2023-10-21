from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import create_short_link
from .validators import valdation_api_field


@app.route('/api/id/', methods=['POST'])
def create_link():
    """View-функция создания новой короткой ссылки."""
    data = valdation_api_field(request.get_json())
    return jsonify(create_short_link(data)), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Получение оригинальной ссылки по короткой ссылке."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(url=url_map.original), 200
