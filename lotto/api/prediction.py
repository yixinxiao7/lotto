import flask
import lotto
import random
import numpy as np


from lotto.api.models.model import RelationModel
# from lotto.db import get_db

@lotto.app.route('/prediction/', methods=['GET'])
def make_prediction():
    """Make a forecase based on current db data."""
    context = {}
    predictor = RelationModel(
                              type_to_instance={}, 
                              firstnumrange_to_num={},
                              horizontal_relations={},
                              vertical_relations={},
                              first_num_freq={},
                              num_to_others_freq={}
                             )
    # teach model
    predictor.get_relations()
    # Phase 1: get model characterization
    model_char = predictor.predict_model_char()
    context['model_char'] = model_char
    # Phase 2: get model
    model = predictor.predict_model(model_char)
    context['model'] = model
    # Phase 3: get numbers
    context['nums'] = predictor.predict_nums(model)
    return flask.jsonify(**context)
