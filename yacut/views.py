from flask import redirect, render_template

from . import app
from .forms import YacutForm
from .models import URLMap
from .validators import valdation_form


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница."""
    form = YacutForm()
    if form.validate_on_submit():
        if valdation_form(form):
            return render_template(
                'index.html', form=form, short=form.custom_id.data
            )
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    """View-функция переадресации на исходный адрес."""
    return redirect(
        URLMap.query.filter_by(short=custom_id).first_or_404().original
    )
