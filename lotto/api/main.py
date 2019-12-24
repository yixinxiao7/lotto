import flask
import lotto

from model import convert_to_model, conv_to_nums
from db import get_db


@lotto.app.route('/api/', methods=['GET','POST'])
def handle_request():
    """Modify or show db."""
    if flask.request.method == 'POST':
        #  add entry to db
        cursor = get_db().cursor()
        date = flask.request.get_json()['date']
        combination = flask.request.get_json()['text']
        comb_nums = conv_to_nums(combination.split())
        model_str = convert_to_model(comb_nums)

        cursor.execute('INSERT INTO combinations (date, val1, val2, val3, val4, val5, model)' +
                       'VALUES (?,?,?,?,?,?,?);',
                       (date, comb_nums[0],comb_nums[1],comb_nums[2],comb_nums[3],comb_nums[4], model_str)
                      )
    else:
        context = {}
        # get entry
        size = flask.requests.args.get("size", type=int)
        all_entries = cursor.execute("SELECT * FROM combinations").fetchall()
        if size == 0:
            # get all entries
            context['entries'] = all_entries
        elif size > 0:
            spec_entries = []
            for i in range(size):
                spec_entries.append(all_entries[i])
            context['entries'] = spec_entries
        else: 
            # catch error
            raise Exception
        return flask.jsonify(**context)
