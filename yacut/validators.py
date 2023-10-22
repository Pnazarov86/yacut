from re import match

from flask import flash

from .constants import ALLOWED_USER_CHARS, CUSTOM_LINK_LENGJT
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


def validation_data(data, api=False):
    """Валидация данных."""
    if api:
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
    else:
        short = data['custom_id']
        if not short:
            short = get_unique_short_id()
        elif URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return None
        return short
    return data
