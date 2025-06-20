from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime, timedelta

logview_bp = Blueprint('logview', __name__)

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

@logview_bp.route('/')
@login_required
def list_logs():
    """List deployment logs with filtering"""
    conn = get_db_connection()
    
    # Get filter parameters
    project_id = request.args.get('project_id', type=int)
    status = request.args.get('status')
    days = request.args.get('days', 7, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Build query
    where_conditions = []
    params = []
    
    if project_id:
        where_conditions.append('dl.project_id = ?')
        params.append(project_id)
    
    if status:
        where_conditions.append('dl.status = ?')
        params.append(status)
    
    if days > 0:
        date_threshold = datetime.now() - timedelta(days=days)
        where_conditions.append('dl.timestamp >= ?')
        params.append(date_threshold.strftime('%Y-%m-%d %H:%M:%S'))
    
    where_clause = ' AND ' + ' AND '.join(where_conditions) if where_conditions else ''
    
    # Get total count
    count_query = f'''
        SELECT COUNT(*) 
        FROM deploy_log dl
        JOIN project p ON dl.project_id = p.id
        {where_clause}
    '''
    total_logs = conn.execute(count_query, params).fetchone()[0]
    
    # Get logs with pagination
    offset = (page - 1) * per_page
    params.extend([per_page, offset])
    
    logs_query = f'''
        SELECT dl.*, p.name as project_name
        FROM deploy_log dl
        JOIN project p ON dl.project_id = p.id
        {where_clause}
        ORDER BY dl.timestamp DESC
        LIMIT ? OFFSET ?
    '''
    logs = conn.execute(logs_query, params).fetchall()
    
    # Get all projects for filter dropdown
    projects = conn.execute('SELECT id, name FROM project ORDER BY name').fetchall()
    
    conn.close()
    
    # Calculate pagination
    total_pages = (total_logs + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return render_template('logs.html',
                         logs=logs,
                         projects=projects,
                         current_filters={
                             'project_id': project_id,
                             'status': status,
                             'days': days
                         },
                         pagination={
                             'page': page,
                             'per_page': per_page,
                             'total': total_logs,
                             'total_pages': total_pages,
                             'has_prev': has_prev,
                             'has_next': has_next,
                             'prev_num': page - 1 if has_prev else None,
                             'next_num': page + 1 if has_next else None
                         })

@logview_bp.route('/view/<int:log_id>')
@login_required
def view_log(log_id):
    """View individual log file content"""
    conn = get_db_connection()
    log_entry = conn.execute('''
        SELECT dl.*, p.name as project_name
        FROM deploy_log dl
        JOIN project p ON dl.project_id = p.id
        WHERE dl.id = ?
    ''', (log_id,)).fetchone()
    conn.close()
    
    if not log_entry:
        flash('Log entry not found.', 'error')
        return redirect(url_for('logview.list_logs'))
    
    # Read log file content
    log_content = ""
    if os.path.exists(log_entry['log_path']):
        try:
            with open(log_entry['log_path'], 'r') as f:
                log_content = f.read()
        except Exception as e:
            log_content = f"Error reading log file: {str(e)}"
    else:
        log_content = "Log file not found."
    
    return render_template('log_detail.html', 
                         log_entry=log_entry, 
                         log_content=log_content)

@logview_bp.route('/download/<int:log_id>')
@login_required
def download_log(log_id):
    """Download log file"""
    from flask import send_file
    
    conn = get_db_connection()
    log_entry = conn.execute('''
        SELECT dl.*, p.name as project_name
        FROM deploy_log dl
        JOIN project p ON dl.project_id = p.id
        WHERE dl.id = ?
    ''', (log_id,)).fetchone()
    conn.close()
    
    if not log_entry:
        flash('Log entry not found.', 'error')
        return redirect(url_for('logview.list_logs'))
    
    if not os.path.exists(log_entry['log_path']):
        flash('Log file not found.', 'error')
        return redirect(url_for('logview.list_logs'))
    
    return send_file(log_entry['log_path'], 
                    as_attachment=True,
                    download_name=f"{log_entry['project_name']}_{log_entry['timestamp']}.log")

@logview_bp.route('/stats')
@login_required
def deployment_stats():
    """Show deployment statistics"""
    conn = get_db_connection()
    
    # Overall stats
    overall_stats = conn.execute('''
        SELECT 
            COUNT(*) as total_deployments,
            SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_deployments,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_deployments,
            SUM(CASE WHEN status = 'started' THEN 1 ELSE 0 END) as running_deployments
        FROM deploy_log
    ''').fetchone()
    
    # Stats by project
    project_stats = conn.execute('''
        SELECT 
            p.name,
            COUNT(dl.id) as total_deployments,
            SUM(CASE WHEN dl.status = 'success' THEN 1 ELSE 0 END) as successful_deployments,
            SUM(CASE WHEN dl.status = 'failed' THEN 1 ELSE 0 END) as failed_deployments,
            MAX(dl.timestamp) as last_deployment
        FROM project p
        LEFT JOIN deploy_log dl ON p.id = dl.project_id
        GROUP BY p.id, p.name
        ORDER BY total_deployments DESC
    ''').fetchall()
    
    # Daily stats for last 7 days
    daily_stats = conn.execute('''
        SELECT 
            DATE(timestamp) as date,
            COUNT(*) as total_deployments,
            SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_deployments,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_deployments
        FROM deploy_log
        WHERE timestamp >= datetime('now', '-7 days')
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('deployment_stats.html',
                         overall_stats=overall_stats,
                         project_stats=project_stats,
                         daily_stats=daily_stats)

@logview_bp.route('/api/logs/<int:log_id>/tail')
@login_required
def tail_log(log_id):
    """Get last N lines of log file (for live updates)"""
    lines = request.args.get('lines', 50, type=int)
    
    conn = get_db_connection()
    log_entry = conn.execute('SELECT log_path FROM deploy_log WHERE id = ?', (log_id,)).fetchone()
    conn.close()
    
    if not log_entry or not os.path.exists(log_entry['log_path']):
        return jsonify({'error': 'Log file not found'}), 404
    
    try:
        with open(log_entry['log_path'], 'r') as f:
            all_lines = f.readlines()
            tail_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            return jsonify({'lines': ''.join(tail_lines)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@logview_bp.route('/cleanup', methods=['POST'])
@login_required
def cleanup_logs():
    """Clean up old log files and database entries"""
    days = request.form.get('days', 30, type=int)
    
    if days < 1:
        flash('Days must be at least 1.', 'error')
        return redirect(url_for('logview.list_logs'))
    
    conn = get_db_connection()
    
    # Get old log entries
    threshold = datetime.now() - timedelta(days=days)
    old_logs = conn.execute('''
        SELECT id, log_path FROM deploy_log 
        WHERE timestamp < ?
    ''', (threshold.strftime('%Y-%m-%d %H:%M:%S'),)).fetchall()
    
    deleted_files = 0
    deleted_entries = 0
    
    # Delete log files
    for log in old_logs:
        if os.path.exists(log['log_path']):
            try:
                os.remove(log['log_path'])
                deleted_files += 1
            except Exception:
                pass  # Continue if file can't be deleted
    
    # Delete database entries
    deleted_entries = conn.execute('''
        DELETE FROM deploy_log 
        WHERE timestamp < ?
    ''', (threshold.strftime('%Y-%m-%d %H:%M:%S'),)).rowcount
    
    conn.commit()
    conn.close()
    
    flash(f'Cleanup completed: {deleted_entries} log entries and {deleted_files} files deleted.', 'success')
    return redirect(url_for('logview.list_logs'))