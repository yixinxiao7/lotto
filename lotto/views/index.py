"""Main view of lotto."""

import flask
import lotto

@lotto.app.route('/', methods=['GET'])
def show_index():
    """Show index page."""
    context = {}
    return flask.render_template('index.html', **context)
