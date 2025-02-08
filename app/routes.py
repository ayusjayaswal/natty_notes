from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import get_db
from app.models import User

auth = Blueprint('auth', __name__)
notes = Blueprint('notes', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.get_by_username(username):
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            'INSERT INTO users (username, password_hash) VALUES (%s, %s)',
            (username, generate_password_hash(password))
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('notes.list_notes'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@notes.route('/')
@login_required
def list_notes():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        'SELECT * FROM notes WHERE user_id = %s ORDER BY created_at DESC',
        (current_user.id,)
    )
    notes = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('notes.html', notes=notes)

@notes.route('/note/new', methods=['POST'])
@login_required
def new_note():
    title = request.form.get('title')
    content = request.form.get('content')
    
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        'INSERT INTO notes (title, content, user_id) VALUES (%s, %s, %s)',
        (title, content, current_user.id)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('notes.list_notes'))

@notes.route('/note/<int:id>/update', methods=['POST'])
@login_required
def update_note(id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        'UPDATE notes SET title = %s, content = %s WHERE id = %s AND user_id = %s',
        (request.form.get('title'), request.form.get('content'), id, current_user.id)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('notes.list_notes'))

@notes.route('/note/<int:id>/delete')
@login_required
def delete_note(id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        'DELETE FROM notes WHERE id = %s AND user_id = %s',
        (id, current_user.id)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('notes.list_notes'))

