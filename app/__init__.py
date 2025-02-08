from flask import Flask
from flask_login import LoginManager
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv

load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def get_db():
    return psycopg2.connect(
        os.getenv('DATABASE_URL'),
        cursor_factory=DictCursor
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    
    # Create tables
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(64) UNIQUE NOT NULL,
            password_hash VARCHAR(256) NOT NULL
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    
    login_manager.init_app(app)
    
    with app.app_context():
        from app.routes import auth, notes
        app.register_blueprint(auth)
        app.register_blueprint(notes)
        init_db()
    
    return app
