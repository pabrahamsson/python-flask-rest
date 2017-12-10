#!/usr/bin/env python

from atomiccounter import AtomicCounter
from flask import Flask
from flask import Response
from flask import jsonify
from flask import request
from healthcheck import HealthCheck, EnvironmentDump
import json
import socket

application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

health = HealthCheck(application, '/health')
envdump = EnvironmentDump(application, '/environment', include_process=False)

counter = AtomicCounter()
paths = [ "/", "/greeting", "/hostinfo" ]
template = "Hello, {0}!"
welcome = "This is my webservice!"

@application.route('/greeting', methods = ['GET'])
def greeting():
    name = 'World'
    if 'name' in request.args:
        name = request.args['name']
    message = {
            'id': counter.increment(),
            'content': template.format(name)
            }
    resp = json_response(message)
    return resp


@application.route('/', methods = ['GET'])
def index(welcome=welcome):
    message = {
            'message':welcome,
            'paths':'[{0}]'.format(str(paths)[1:-1])
            }
    resp = json_response(message, True)
    return resp


@application.route('/hostinfo', methods = ['GET'])
def hostinfo():
    message = {
            'hostname': socket.gethostname()
            }
    resp = json_response(message)
    return resp


def json_response(message, sort=False):
    """
    response = jsonify(
            json.dumps(
                message,
                separators=(',', ':'),
                sort_keys=sort
                )
            )
    """
    response = jsonify(message)
    response.status_code=200
    return response


if __name__ == '__main__':
    application.run()
