from flask import Flask, render_template, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
from auth import auth_bp
from project import project_bp  
from logview import logview_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
app.config['DATABASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'deploy.db')
app.config['LOG_DIR'] = '/opt/deploy/logs'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(project_bp, url_prefix='/projects')
app.register_blueprint(logview_bp, url_prefix='/logs')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database if it doesn't exist"""
    if not os.path.exists(app.config['DATABASE']):
        os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
        # Initialize database in current directory
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from deploy.init_db import create_database
        create_database(app.config['DATABASE'])

def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    
    # Get projects count
    projects_count = conn.execute('SELECT COUNT(*) FROM project').fetchone()[0]
    
    # Get recent deployments
    recent_deployments = conn.execute('''
        SELECT dl.*, p.name as project_name
        FROM deploy_log dl
        JOIN project p ON dl.project_id = p.id
        ORDER BY dl.timestamp DESC
        LIMIT 10
    ''').fetchall()
    
    # Get deployment stats
    today = datetime.now().strftime('%Y-%m-%d')
    stats = conn.execute('''
        SELECT 
            COUNT(*) as total_deployments,
            SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_deployments,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_deployments,
            SUM(CASE WHEN DATE(timestamp) = ? THEN 1 ELSE 0 END) as today_deployments
        FROM deploy_log
    ''', (today,)).fetchone()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         projects_count=projects_count,
                         recent_deployments=recent_deployments,
                         stats=stats)

@app.route('/dashboard')
@login_required
def dashboard():
    """Redirect to index"""
    return redirect(url_for('index'))

@app.context_processor
def inject_user():
    """Inject user info into all templates"""
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM user WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        return dict(current_user=user)
    return dict(current_user=None)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)