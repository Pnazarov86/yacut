from flask import flash, redirect, render_template

from . import app
from .error_handlers import CreateLinkException
from .forms import YacutForm
from .models import URLMap
from .utils import create_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница."""
    form = YacutForm()
    if form.validate_on_submit():
        try:
            create_short_link({
                'url': form.original_link.data,
                'custom_id': form.custom_id.data
            })
            return render_template(
                'index.html', form=form, short=form.custom_id.data
            )
        except CreateLinkException as error:
            flash(str(error))
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    """View-функция переадресации на исходный адрес."""
    return redirect(
        URLMap.query.filter_by(short=custom_id).first_or_404().original
    )
