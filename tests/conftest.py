import pytest
from app import create_app
from instance import db

@pytest.fixture
def app():
    app = create_app(testing=True)
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()