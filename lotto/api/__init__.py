"""Server w/ REST API."""

from lotto.api.index import handle_request, handle_file_upload, handle_delete
from lotto.api.prediction import make_prediction