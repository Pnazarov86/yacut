from flask import redirect, render_template
from .utils import create_short_link

from . import app
from .forms import YacutForm
from .models import URLMap
from .validators import validation_data


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница."""
    form = YacutForm()
    if form.validate_on_submit():
        short = validation_data(form.data)
        if short:
            create_short_link(
                {'url': form.original_link.data, 'custom_id': short}
            )
            return render_template('index.html', form=form, short=short)
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    """View-функция переадресации на исходный адрес."""
    return redirect(
        URLMap.query.filter_by(short=custom_id).first_or_404().original
    )
