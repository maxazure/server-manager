# Gunicorn configuration file
# Usage: gunicorn --config gunicorn.conf.py app:app

import multiprocessing
import os

# Server socket
bind = "127.0.0.1:5000"
backlog = 2048

# Worker processes
workers = min(multiprocessing.cpu_count() * 2 + 1, 8)
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Request handling
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Logging
accesslog = "/var/log/flask-deploy/access.log"
errorlog = "/var/log/flask-deploy/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "flask-deploy"

# Server mechanics
daemon = False  # Set to True if running as daemon
pidfile = "/var/run/flask-deploy.pid"
user = None  # Set by systemd
group = None  # Set by systemd
tmp_upload_dir = "/tmp"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
worker_tmp_dir = "/dev/shm" if os.path.exists("/dev/shm") else "/tmp"

# Hooks
def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def worker_exit(server, worker):
    server.log.info("Worker exited (pid: %s)", worker.pid)

def post_worker_init(worker):
    worker.log.info("Worker initialized (pid: %s)", worker.pid)