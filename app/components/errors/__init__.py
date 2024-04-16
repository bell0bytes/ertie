import flask
bpErrors = flask.Blueprint('errors', __name__)
from . import handlers
