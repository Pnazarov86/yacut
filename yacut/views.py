import random

from flask import flash, redirect, render_template

from . import app, db
from .constants import ALLOWED_AUTO_CHARS, AUTO_lINK_LENGJT
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


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция главной страницы."""
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


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    """View-функция переадресации на исходный адрес."""
    url_map = URLMap.query.filter_by(short=custom_id).first_or_404()
    return redirect(url_map.original)