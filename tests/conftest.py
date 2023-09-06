import pytest
from app import create_app
from instance import db

@pytest.fixture
def app():
    app = create_app(status='development')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client