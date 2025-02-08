import pytest
import psycopg2
from psycopg2.extras import DictCursor
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    
    # Setup test database
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='db'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create test database
    cur.execute('DROP DATABASE IF EXISTS test_notes')
    cur.execute('CREATE DATABASE test_notes')
    
    cur.close()
    conn.close()
    
    # Use test database
    app.config['DATABASE_URL'] = 'postgresql://postgres:postgres@db:5432/test_notes'
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Verify user was created
    conn = psycopg2.connect(
        'postgresql://postgres:postgres@db:5432/test_notes',
        cursor_factory=DictCursor
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', ('testuser',))
    assert cur.fetchone() is not None
    cur.close()
    conn.close()

