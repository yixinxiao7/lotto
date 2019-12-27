import flask
import lotto

from lotto.api.model import convert_to_model, conv_to_nums
from lotto.db import get_db


@lotto.app.route('/api/', methods=['GET','POST'])
def handle_request():
    """Modify or show db."""
    db = get_db()
    cursor = db.cursor()
    if flask.request.method == 'POST':
        #  add entry to db
        date = flask.request.get_json()['date']
        combination = flask.request.get_json()['text']
        comb_nums = conv_to_nums(combination.split())
        model_str = convert_to_model(comb_nums)

        cursor.execute("INSERT INTO combinations(date, val1, val2, val3, val4, val5, model)" +
                       "VALUES ('" + date + "'," + str(comb_nums[0]) +
                       "," + str(comb_nums[1]) + "," + str(comb_nums[2]) +
                       "," + str(comb_nums[3]) + "," + str(comb_nums[4]) +
                       ",'" + model_str + "');"
                      )
        context = {}
        context['model'] = model_str

        return flask.jsonify(**context)
    else:
        context = {}
        # get entry
        size = flask.request.args.get("size", type=int)
        try:
            all_entries = cursor.execute("SELECT * FROM combinations ORDER BY date DESC").fetchall()
            if size == 0:
                # get all entries
                context['entries'] = all_entries
            elif size > 0:
                # adjust if size > num entries
                if len(all_entries) < size:
                    size = len(all_entries)
                spec_entries = []
                for i in range(size):
                    spec_entries.append(all_entries[i])
                context['entries'] = spec_entries
            else: 
                # catch error
                raise Exception
        except:
            context['entries'] = []

        return flask.jsonify(**context)
