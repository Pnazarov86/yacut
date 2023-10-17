from flask import redirect, request

from . import app
from .models import URLMap
from .utils import index_page


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция главной страницы."""
    return index_page(request)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    """View-функция переадресации на исходный адрес."""
    return redirect(
        URLMap.query.filter_by(short=custom_id).first_or_404().original
    )
