"""Lotto package initializer."""

import flask

app = flask.Flask(__name__)

app.config.from_object('lotto.config')

app.config.from_envvar('LOTTO_SETTINGS', silent=True)

# import packages
import lotto.api
import lotto.views
import lotto.db
