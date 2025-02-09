# tests/test_app.py
import pytest
from app import create_app, db
from app.models import User, Note

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost:5432/test_db'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        assert User.query.filter_by(username='testuser').first() is not None
