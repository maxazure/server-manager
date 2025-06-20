#!/usr/bin/env python3

import sqlite3
import hashlib
import os
from datetime import datetime

def create_database(db_path=None):
    """Create SQLite database and tables"""
    
    if db_path is None:
        # Default to Flask app directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        flask_app_dir = os.path.join(os.path.dirname(script_dir), 'flask_app')
        db_path = os.path.join(flask_app_dir, 'data', 'deploy.db')
    
    # Create data directory if not exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create project table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            repo_url TEXT NOT NULL,
            branch TEXT NOT NULL DEFAULT 'main',
            deploy_dir TEXT NOT NULL,
            secret TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create deploy_log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deploy_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL CHECK (status IN ('started', 'success', 'failed')),
            log_path TEXT NOT NULL,
            commit_id TEXT,
            branch TEXT,
            FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_deploy_log_project_id ON deploy_log(project_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_deploy_log_timestamp ON deploy_log(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_deploy_log_status ON deploy_log(status)')
    
    conn.commit()
    print("Database tables created successfully")
    
    # Insert default admin user if not exists
    cursor.execute('SELECT COUNT(*) FROM user WHERE username = ?', ('admin',))
    if cursor.fetchone()[0] == 0:
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute(
            'INSERT INTO user (username, password_hash) VALUES (?, ?)',
            ('admin', password_hash)
        )
        conn.commit()
        print("Default admin user created (username: admin, password: admin123)")
    
    # Insert sample projects if not exists
    sample_projects = [
        {
            'name': 'project1',
            'repo_url': 'https://github.com/username/project1.git',
            'branch': 'main',
            'deploy_dir': '/var/www/project1',
            'secret': 'your-webhook-secret-project1'
        },
        {
            'name': 'project2', 
            'repo_url': 'https://github.com/username/project2.git',
            'branch': 'develop',
            'deploy_dir': '/var/www/project2',
            'secret': 'your-webhook-secret-project2'
        }
    ]
    
    for project in sample_projects:
        cursor.execute('SELECT COUNT(*) FROM project WHERE name = ?', (project['name'],))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO project (name, repo_url, branch, deploy_dir, secret)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                project['name'],
                project['repo_url'], 
                project['branch'],
                project['deploy_dir'],
                project['secret']
            ))
            print(f"Sample project '{project['name']}' added")
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == '__main__':
    create_database()