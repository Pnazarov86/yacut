from datetime import datetime

from flask import url_for

from . import db
from .constants import ORIGINAL_LINK_LENGJT, CUSTOM_lINK_LENGJT


class URLMap(db.Model):
    """Модель конвертации ссылок."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGJT), nullable=False)
    short = db.Column(db.String(CUSTOM_lINK_LENGJT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Метод - сериализатор."""
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', custom_id=self.short, _external=True
            )
        )

    def from_dict(self, data):
        """Метод - десериализатор."""
        self.original = data['url']
        self.short = data['custom_id']