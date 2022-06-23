from flask import Flask, Response
from utils import prepare_response

class EndpointAction(object):

    def __init__(self, action):
        self.__action = action

    def __call__(self, *args):
        return self.__action()


class ModelApi():
    app = None

    def __init__(self, name):
        self.app = Flask(name)
        self.add_endpoint('/ping', lambda: 'Pong!!!', ['GET', 'POST'])

    def add_endpoint(self, endpoint=None, handler=None, methods=['GET']):
        self.app.add_url_rule(endpoint, '_'.join(endpoint[1:].split('/')), \
            EndpointAction(handler), methods=methods)