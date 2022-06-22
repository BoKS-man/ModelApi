from flask import Flask, Response
from utils import prepare_response

class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = prepare_response()

    def __call__(self, *args):
        self.action()
        return self.response

class ModelApi():
    app = None

    def __init__(self, name):
        self.app = Flask(name)
        self.add_endpoint('/ping', 'Pong!!!', ['GET', 'POST'])

    def add_endpoint(self, endpoint=None, handler=None, methods=['GET']):
        self.app.add_url_rule(endpoint, '_'.join(endpoint[1:].split('/')), \
            EndpointAction(handler), methods=methods)