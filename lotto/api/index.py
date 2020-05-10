import flask
import lotto
import xlrd
import os
import base64

from lotto.api.model import convert_to_model, conv_to_nums, convert_to_ranges
from lotto.db import get_db


@lotto.app.route('/api/', methods=['GET','POST'])
def handle_request():
    """Modify or show db."""
    db = get_db()
    cursor = db.cursor()
    if flask.request.method == 'POST':
        #  add entry to db
        year = flask.request.get_json()['year']
        date = flask.request.get_json()['date']
        combination = flask.request.get_json()['text']
        comb_nums = conv_to_nums(combination.split())
        model_ranges = convert_to_ranges(comb_nums)
        model_str = convert_to_model(comb_nums)

        cursor.execute("INSERT INTO combinations(year, date, val1, val2, val3, val4, val5, model, model_ranges)" +
                       "VALUES ('" + year + "','" + date + "'," + str(comb_nums[0]) +
                       "," + str(comb_nums[1]) + "," + str(comb_nums[2]) +
                       "," + str(comb_nums[3]) + "," + str(comb_nums[4]) +
                       ",'" + model_str + "','" + model_ranges + "');"
                      )
        context = {}
        context['model'] = model_str

        return flask.jsonify(**context)
    else:
        context = {}
        # get entry
        size = flask.request.args.get("size", type=int)
        try:
            all_entries = cursor.execute("SELECT * FROM combinations ORDER BY id DESC").fetchall()
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


@lotto.app.route('/excelupload/', methods=['GET','POST'])
def handle_file_upload():
    """Add excel file to data directory and updates database."""
    db = get_db()
    cursor = db.cursor()

    # get file data
    xfile = flask.request.get_json()['file']
    data_url_idx = xfile.find(',')
    data_url = xfile[data_url_idx+1:]
    file_data = base64.b64decode(data_url)

    # add to /data
    cwd = os.getcwd()
    data_path = os.path.join(cwd, 'data/')
    # ascertain data directory exists first
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    path = os.path.join(cwd, 'data/data.xlsx')
    # remove old data file
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'wb') as f:
        f.write(file_data)

    # update database
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)
    year = ""
    month = ""

    for row in range(sheet.nrows):
        if sheet.cell_value(row, 0) != 'x':
            # first column
            date = sheet.cell_value(row, 0)
            if len(str(date)) == 6:
                year_month = date.split('-')
                year = year_month[0]
                month = year_month[1]
            else:
                month = str(date)
            # all other columns
            combination = []
            for col in range(1, sheet.ncols):
                combination.append(sheet.cell_value(row, col))
            comb_nums = conv_to_nums(combination)
            model_ranges = convert_to_ranges(comb_nums)
            model_str = convert_to_model(comb_nums)

            # insert into db
            cursor.execute("INSERT INTO combinations(year, date, val1, val2, val3, val4, val5, model, model_ranges)" +
                        "VALUES ('" + year + "','" + month + "'," + str(comb_nums[0]) +
                        "," + str(comb_nums[1]) + "," + str(comb_nums[2]) +
                        "," + str(comb_nums[3]) + "," + str(comb_nums[4]) +
                        ",'" + model_str + "','" + model_ranges + "');"
                        )
    # ack
    context = {} 
    return flask.jsonify(**context)
