#!/usr/bin/env python3

import sqlite3
import argparse
import sys
import os
from datetime import datetime

def get_db_path():
    """Get database path from Flask app directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    flask_app_dir = os.path.join(os.path.dirname(script_dir), 'flask_app')
    return os.path.join(flask_app_dir, 'data', 'deploy.db')

def write_log_entry(project_name, status, log_path, commit_id=None, branch=None):
    """Write deployment log entry to database"""
    
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get project_id by name
        cursor.execute('SELECT id FROM project WHERE name = ?', (project_name,))
        result = cursor.fetchone()
        
        if not result:
            print(f"Error: Project '{project_name}' not found in database", file=sys.stderr)
            return False
            
        project_id = result[0]
        
        # Insert log entry
        cursor.execute('''
            INSERT INTO deploy_log (project_id, status, log_path, commit_id, branch)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_id, status, log_path, commit_id, branch))
        
        conn.commit()
        conn.close()
        
        print(f"Log entry written: project={project_name}, status={status}, log={log_path}")
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Write deployment log to database')
    parser.add_argument('--project-name', required=True, help='Project name')
    parser.add_argument('--status', required=True, choices=['started', 'success', 'failed'], 
                       help='Deployment status')
    parser.add_argument('--log-path', required=True, help='Path to log file')
    parser.add_argument('--commit-id', help='Git commit ID')
    parser.add_argument('--branch', help='Git branch name')
    
    args = parser.parse_args()
    
    success = write_log_entry(
        project_name=args.project_name,
        status=args.status,
        log_path=args.log_path,
        commit_id=args.commit_id,
        branch=args.branch
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()