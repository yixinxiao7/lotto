import flask
import lotto
import random

from lotto.api.aux.relations import RelationGenerator
from lotto.db import get_db

@lotto.app.route('/prediction/', methods=['GET'])
def make_prediction():
    """Modify or show db."""
    db = get_db()
    cursor = db.cursor()

    context = {}
    all_poss = "ABCDE"
    # get model number
    relation_generator = RelationGenerator(type_to_instance={})
    relation_generator.get_relations()
    model = 'A'
    letter_idx = 0
    while len(model) != 4:
        model += all_pos[letter_idx]
        first_poss = model
        freq1 = relation_generator.get_frequency(first_poss)
        model[len(model)-1] = all_pos[letter_idx+1]  # might go out of bounds?
        second_poss = model
        freq2 = relation_generator.get_frequency(second_poss)
        dem = freq1 + freq2  # float
        model = random.choices([first_poss, second_poss], weights=[(freq1/float(dem)), (freq2/float(dem))], k=1)
        if model == second_poss:
            letter_idx += 1
    
    context['model'] = model

    return flask.jsonify(**context)
