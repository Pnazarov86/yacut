import random

from . import db
from .constants import ALLOWED_AUTO_CHARS, AUTO_LINK_LENGJT
from .error_handlers import YacutDefinitionException
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
        url_map = URLMap()
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()
        return url_map.to_dict()
    except Exception as error:
        raise YacutDefinitionException(f'Ошибка в работе функции {error}')
