from flask import flash, redirect, render_template

from . import app
from .forms import YacutForm
from .models import URLMap
from .utils import create_short_link, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница."""
    form = YacutForm()
    if form.validate_on_submit():
        data = {
            'url': form.original_link.data, 'custom_id': form.custom_id.data
        }
        if not data['custom_id']:
            data['custom_id'] = get_unique_short_id()
        elif URLMap.query.filter_by(short=data['custom_id']).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        create_short_link(data)
        return render_template(
            'index.html', form=form, short=data['custom_id']
        )
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    """View-функция переадресации на исходный адрес."""
    return redirect(
        URLMap.query.filter_by(short=custom_id).first_or_404().original
    )
