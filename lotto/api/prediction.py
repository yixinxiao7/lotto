import flask
import lotto


from lotto.db import get_db

@lotto.app.route('/prediction/', methods=['GET'])
def make_prediction():
    """Modify or show db."""
    db = get_db()
    cursor = db.cursor()

    context = {}
    # get model number
    
    model = 0
    context['model'] = model

    return flask.jsonify(**context)
