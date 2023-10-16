from flask import jsonify, request

from . import app, db
from .models import URLMap
from .validators import valdation_id, valdation_link


@app.route('/api/id/', methods=['POST'])
def create_url():
    """Cоздание новой короткой ссылки."""
    data = valdation_link(request)
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    """Получение оригинальной ссылки по короткой ссылке."""
    url_map = valdation_id(short_id)
    return jsonify(url=url_map.original), 200
