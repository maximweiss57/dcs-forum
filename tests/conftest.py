import pytest
from app import create_app
from instance import db

@pytest.fixture
def app():
    _app = create_app(status='testing')
    with _app.app_context():
        db.create_all()
    yield _app


@pytest.fixture
def client(app):
    return app.test_client()
