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
    model = predictor.predict_model_char()
    context['model'] = model
    # TODO: choose best model

    return flask.jsonify(**context)
