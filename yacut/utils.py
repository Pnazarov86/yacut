import random
from re import match

from . import db
from .constants import (
    ALLOWED_AUTO_CHARS, ALLOWED_USER_CHARS,
    AUTO_LINK_LENGJT, CUSTOM_LINK_LENGJT
)
from .error_handlers import CreateLinkException, InvalidAPIUsage
from .models import URLMap


def get_unique_short_id():
    """Функция формирования коротких ссылок."""
    short_link = ''.join(
        random.choice(ALLOWED_AUTO_CHARS) for i in range(AUTO_LINK_LENGJT)
    )
    if URLMap.query.filter_by(short=short_link).first():
        short_link = get_unique_short_id()
    return short_link


def create_short_link(data):
    """Создание новой короткой ссылки."""
    try:
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
        elif not match(
            ALLOWED_USER_CHARS, short_id
        ) or len(short_id) > CUSTOM_LINK_LENGJT:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        url_map = URLMap()
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()
        return url_map.to_dict()
    except ValueError as error:
        raise CreateLinkException(f'Ошибка создания ссылки {error}')
