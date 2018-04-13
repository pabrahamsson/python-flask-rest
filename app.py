from connexion.resolver import RestyResolver
from healthcheck import HealthCheck
from flask import redirect
from prometheus_client import generate_latest
import connexion

application = connexion.App(__name__, specification_dir='swagger/')
application.add_api('api.yaml', resolver=RestyResolver('api'))
health = HealthCheck(application, '/health')


@application.route('/')
def index():
    return redirect('/v1/ui/', code=301)


@application.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200


if __name__ == '__main__':
    application.run(port=8080)
