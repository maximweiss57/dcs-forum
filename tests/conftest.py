import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('sqlite://')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
