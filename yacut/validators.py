from re import match

from .constants import ALLOWED_USER_CHARS, CUSTOM_lINK_LENGJT
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


def valdation_link(request):
    """Проверяеят заполнение полей."""
    data = request.get_json()
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
    return data


def valdation_id(short_id):
    """Проверяеят наличие ссылки в БД."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return url_map
