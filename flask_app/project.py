from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
import secrets
import string

project_bp = Blueprint('project', __name__)

def get_db_connection():
    """Get database connection"""
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'deploy.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

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

def generate_secret(length=32):
    """Generate random secret for webhook"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@project_bp.route('/')
@login_required
def list_projects():
    """List all projects"""
    conn = get_db_connection()
    projects = conn.execute('''
        SELECT p.*, 
               COUNT(dl.id) as deployment_count,
               MAX(dl.timestamp) as last_deployment,
               SUM(CASE WHEN dl.status = 'success' THEN 1 ELSE 0 END) as successful_deployments,
               SUM(CASE WHEN dl.status = 'failed' THEN 1 ELSE 0 END) as failed_deployments
        FROM project p
        LEFT JOIN deploy_log dl ON p.id = dl.project_id
        GROUP BY p.id
        ORDER BY p.name
    ''').fetchall()
    conn.close()
    
    return render_template('projects.html', projects=projects)

@project_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """Add new project"""
    if request.method == 'POST':
        name = request.form['name'].strip()
        repo_url = request.form['repo_url'].strip()
        branch = request.form['branch'].strip() or 'main'
        deploy_dir = request.form['deploy_dir'].strip()
        secret = request.form['secret'].strip() or generate_secret()
        
        if not name or not repo_url or not deploy_dir:
            flash('Name, repository URL, and deployment directory are required.', 'error')
            return render_template('project_form.html', action='Add', project=None)
        
        conn = get_db_connection()
        
        # Check if project name already exists
        existing = conn.execute('SELECT id FROM project WHERE name = ?', (name,)).fetchone()
        if existing:
            flash('Project name already exists.', 'error')
            conn.close()
            return render_template('project_form.html', action='Add', project=None)
        
        try:
            conn.execute('''
                INSERT INTO project (name, repo_url, branch, deploy_dir, secret)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, repo_url, branch, deploy_dir, secret))
            conn.commit()
            
            # Create deployment script
            create_deployment_script(name, repo_url, branch, deploy_dir)
            
            flash('Project added successfully!', 'success')
            return redirect(url_for('project.list_projects'))
            
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('project_form.html', action='Add', project=None)

@project_bp.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit existing project"""
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM project WHERE id = ?', (project_id,)).fetchone()
    
    if not project:
        flash('Project not found.', 'error')
        conn.close()
        return redirect(url_for('project.list_projects'))
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        repo_url = request.form['repo_url'].strip()
        branch = request.form['branch'].strip() or 'main'
        deploy_dir = request.form['deploy_dir'].strip()
        secret = request.form['secret'].strip()
        
        if not name or not repo_url or not deploy_dir or not secret:
            flash('All fields are required.', 'error')
            conn.close()
            return render_template('project_form.html', action='Edit', project=project)
        
        # Check if name is taken by another project
        existing = conn.execute(
            'SELECT id FROM project WHERE name = ? AND id != ?', 
            (name, project_id)
        ).fetchone()
        if existing:
            flash('Project name already exists.', 'error')
            conn.close()
            return render_template('project_form.html', action='Edit', project=project)
        
        try:
            conn.execute('''
                UPDATE project 
                SET name = ?, repo_url = ?, branch = ?, deploy_dir = ?, secret = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (name, repo_url, branch, deploy_dir, secret, project_id))
            conn.commit()
            
            # Update deployment script
            create_deployment_script(name, repo_url, branch, deploy_dir)
            
            flash('Project updated successfully!', 'success')
            return redirect(url_for('project.list_projects'))
            
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            conn.close()
    
    conn.close()
    return render_template('project_form.html', action='Edit', project=project)

@project_bp.route('/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    """Delete project"""
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM project WHERE id = ?', (project_id,)).fetchone()
    
    if not project:
        flash('Project not found.', 'error')
        conn.close()
        return redirect(url_for('project.list_projects'))
    
    try:
        # Delete deployment logs first (foreign key constraint)
        conn.execute('DELETE FROM deploy_log WHERE project_id = ?', (project_id,))
        # Delete project
        conn.execute('DELETE FROM project WHERE id = ?', (project_id,))
        conn.commit()
        
        # Remove deployment script
        script_path = f'/opt/deploy/scripts/deploy_{project["name"]}.sh'
        if os.path.exists(script_path):
            os.remove(script_path)
        
        flash('Project deleted successfully!', 'success')
        
    except sqlite3.Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('project.list_projects'))

@project_bp.route('/regenerate-secret/<int:project_id>', methods=['POST'])
@login_required
def regenerate_secret(project_id):
    """Regenerate webhook secret"""
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM project WHERE id = ?', (project_id,)).fetchone()
    
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'})
    
    new_secret = generate_secret()
    
    try:
        conn.execute(
            'UPDATE project SET secret = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (new_secret, project_id)
        )
        conn.commit()
        return jsonify({'success': True, 'secret': new_secret})
        
    except sqlite3.Error as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        conn.close()

def create_deployment_script(name, repo_url, branch, deploy_dir):
    """Create deployment script for project"""
    script_content = f'''#!/bin/bash

# Deploy script for {name}
# Arguments: $1=repository_name, $2=ref, $3=commit_id

PROJECT_NAME="{name}"
REPO_URL="{repo_url}"
BRANCH="{branch}"
DEPLOY_DIR="{deploy_dir}"
LOG_DIR="/opt/deploy/logs"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="${{LOG_DIR}}/${{PROJECT_NAME}}_${{TIMESTAMP}}.log"

# Create log directory if not exists
mkdir -p "$LOG_DIR"

# Function to log with timestamp
log() {{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}}

# Function to log and update database
log_and_update_db() {{
    local status=$1
    local message=$2
    log "$message"
    python3 "$(dirname "$(dirname "$0")")/log_writer.py" --project-name "$PROJECT_NAME" --status "$status" --log-path "$LOG_FILE"
}}

log "========== Starting deployment for $PROJECT_NAME =========="
log "Repository: $1, Ref: $2, Commit: $3"

# Update database with deployment start
log_and_update_db "started" "Deployment started"

# Change to deployment directory
cd "$DEPLOY_DIR" || {{
    log_and_update_db "failed" "Failed to change to deployment directory: $DEPLOY_DIR"
    exit 1
}}

# Run pre-deployment script if exists
if [ -f "/opt/deploy/scripts/pre_deploy.sh" ]; then
    log "Running pre-deployment script..."
    if bash /opt/deploy/scripts/pre_deploy.sh "$PROJECT_NAME" 2>&1 | tee -a "$LOG_FILE"; then
        log "Pre-deployment script completed successfully"
    else
        log_and_update_db "failed" "Pre-deployment script failed"
        exit 1
    fi
fi

# Git pull
log "Pulling latest changes from $BRANCH branch..."
if git pull origin "$BRANCH" 2>&1 | tee -a "$LOG_FILE"; then
    log "Git pull completed successfully"
else
    log_and_update_db "failed" "Git pull failed"
    exit 1
fi

# Install dependencies based on project type
if [ -f "package.json" ]; then
    log "Installing npm dependencies..."
    if npm install 2>&1 | tee -a "$LOG_FILE"; then
        log "npm install completed successfully"
    else
        log_and_update_db "failed" "npm install failed"
        exit 1
    fi
    
    # Build if build script exists
    if npm run build --silent 2>/dev/null; then
        log "Building project..."
        if npm run build 2>&1 | tee -a "$LOG_FILE"; then
            log "Build completed successfully"
        else
            log_and_update_db "failed" "Build failed"
            exit 1
        fi
    fi
elif [ -f "requirements.txt" ]; then
    log "Installing Python dependencies..."
    if pip3 install -r requirements.txt 2>&1 | tee -a "$LOG_FILE"; then
        log "pip install completed successfully"
    else
        log_and_update_db "failed" "pip install failed"
        exit 1
    fi
fi

# Restart services if needed
if systemctl is-active --quiet "${{PROJECT_NAME}}.service"; then
    log "Restarting ${{PROJECT_NAME}} service..."
    if sudo systemctl restart "${{PROJECT_NAME}}.service" 2>&1 | tee -a "$LOG_FILE"; then
        log "Service restarted successfully"
    else
        log_and_update_db "failed" "Service restart failed"
        exit 1
    fi
fi

# Run post-deployment script if exists
if [ -f "/opt/deploy/scripts/post_deploy.sh" ]; then
    log "Running post-deployment script..."
    if bash /opt/deploy/scripts/post_deploy.sh "$PROJECT_NAME" 2>&1 | tee -a "$LOG_FILE"; then
        log "Post-deployment script completed successfully"
    else
        log_and_update_db "failed" "Post-deployment script failed"
        exit 1
    fi
fi

log_and_update_db "success" "Deployment completed successfully"
log "========== Deployment finished =========="

exit 0'''

    script_path = f'/opt/deploy/scripts/deploy_{name}.sh'
    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(script_path, 0o755)