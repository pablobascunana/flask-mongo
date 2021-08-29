import os
import pytest
from dotenv import load_dotenv

load_dotenv('../.env.testing')

from flask import Flask
from flask_restful import Api
from resources.status import IsAlive, Version, check_database_is_alive


@pytest.fixture
def client():
    app = Flask(__name__)
    with app.test_client() as client:
        api = Api(app)
        api.add_resource(Version, "/version")
        api.add_resource(IsAlive, "/isalive")
        yield client


def test_version(client):
    response = client.get('/version')
    assert b'##VersionNumber##' in response.data


def test_is_alive():
    status = check_database_is_alive(os.getenv('DATABASE'))
    pytest.set_trace()
    assert status
