import flask
import lotto
import random
import numpy as numpy


from lotto.api.aux.relations import RelationGenerator
from sklearn.linear_model import LinearRegression
from lotto.api.aux.model import convert_model_to_coordinates, convert_coordinates_to_model
# from lotto.db import get_db

@lotto.app.route('/prediction/', methods=['GET'])
def make_prediction():
    """Modify or show db."""
    context = {}
    all_poss = "ABCDE"
    # get model number
    relation_generator = RelationGenerator(type_to_instance={})
    relation_generator.get_relations()
    model = 'A'
    letter_idx = 0
    while len(model) != 4:
        model += all_poss[letter_idx]
        first_poss = model
        freq1 = relation_generator.get_frequency(first_poss)
        model[len(model)-1] = all_poss[letter_idx+1]  # might go out of bounds?
        second_poss = model
        freq2 = relation_generator.get_frequency(second_poss)
        dem = freq1 + freq2  # float
        model = random.choices([first_poss, second_poss], weights=[(freq1/float(dem)), (freq2/float(dem))], k=1)
        if model == second_poss:
            letter_idx += 1
    print(model)
    # convert model to coordinate
    pred_coord = convert_model_to_coordinates(model)
    # linear regression
    X = np.asarray(relation_generator.X)  # array of tuples
    y = np.asarray(relation_generator.y)  # array of integers
    reg = LinearRegression().fit(X, y)
    # score
    print(reg.score(X,y))
    num_model = reg.predict(np.array([pred_coord]))
    context['model'] = convert_coordinates_to_model(num_model)
    # TODO: choose best model

    return flask.jsonify(**context)
