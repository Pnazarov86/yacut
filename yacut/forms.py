from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .constants import CUSTOM_LINK_LENGJT, ORIGINAL_LINK_LENGJT


class YacutForm(FlaskForm):
    """Форма для создания ссылок."""
    original_link = URLField(
        'Введите длинную ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=ORIGINAL_LINK_LENGJT)
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=CUSTOM_LINK_LENGJT), Optional()]
    )
    submit = SubmitField('Добавить')
