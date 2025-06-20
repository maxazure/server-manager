from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib

auth_bp = Blueprint('auth', __name__)

def get_db_connection():
    """Get database connection"""
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'deploy.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        conn.close()
        
        if user and user['password_hash'] == hashlib.sha256(password.encode()).hexdigest():
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """User logout"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not password or not confirm_password:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        
        # Check if username already exists
        existing_user = conn.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if existing_user:
            flash('Username already exists.', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn.execute(
            'INSERT INTO user (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Change user password"""
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if not current_password or not new_password or not confirm_password:
            flash('All fields are required.', 'error')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('change_password.html')
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('change_password.html')
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM user WHERE id = ?', (session['user_id'],)
        ).fetchone()
        
        current_password_hash = hashlib.sha256(current_password.encode()).hexdigest()
        if user['password_hash'] != current_password_hash:
            flash('Current password is incorrect.', 'error')
            conn.close()
            return render_template('change_password.html')
        
        # Update password
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        conn.execute(
            'UPDATE user SET password_hash = ? WHERE id = ?',
            (new_password_hash, session['user_id'])
        )
        conn.commit()
        conn.close()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('change_password.html')