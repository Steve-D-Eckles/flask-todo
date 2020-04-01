import pytest

from flasktodo import create_app
from flasktodo import db


@pytest.fixture
def app():
    """Create an app configured for tests."""

    app = create_app({
        'TESTING': True,
        'DB_URL': "postgresql://flasktodo_user@localhost/flasktodo_test"
    })

    # Using app context, create database tables and fill with mock data
    with app.app_context():
        db.init_db()
        db.mock_db()

    yield app


@pytest.fixture
def client(app):
    """Using test app, create and return a client object."""

    return app.test_client()


@pytest.fixture
def runner(app):
    """Using test app, create and return a CLI runner object."""

    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client= client

    def login(self, username='test', password='password'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
