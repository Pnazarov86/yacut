import random
from re import match

from flask import flash, jsonify, render_template

from . import db
from .constants import (
    ALLOWED_AUTO_CHARS, ALLOWED_USER_CHARS,
    AUTO_lINK_LENGJT, CUSTOM_lINK_LENGJT
)
from .error_handlers import InvalidAPIUsage
from .forms import YacutForm
from .models import URLMap


def get_unique_short_id():
    """Функция вормирования коротких ссылок."""
    short_link = ''.join(
        random.choice(ALLOWED_AUTO_CHARS) for i in range(AUTO_lINK_LENGJT)
    )
    if URLMap.query.filter_by(short=short_link).first():
        short_link = get_unique_short_id()
    return short_link


def create_short_link(data):
    """Создание новой короткой ссылки."""
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    short_id = data.get('custom_id')
    if not short_id:
        data['custom_id'] = get_unique_short_id()
    elif URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    elif not match(ALLOWED_USER_CHARS, short_id) or len(short_id) > CUSTOM_lINK_LENGJT:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


def get_original_url(short_id):
    """получение оригинальной ссылки по короткой ссылке."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(url=url_map.original), 200


def index_page(request):
    """Главная страница."""
    form = YacutForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        elif URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('index.html', form=form, short=short)
    return render_template('index.html', form=form)
