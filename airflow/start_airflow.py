# start_airflow.py

import subprocess
import sys
import os
from pathlib import Path

def setup_airflow():
    """Setup and start Airflow services"""
    
    # Create airflow directories
    airflow_home = Path.home() / 'airflow'
    (airflow_home / 'dags').mkdir(exist_ok=True)
    (airflow_home / 'logs').mkdir(exist_ok=True)
    (airflow_home / 'plugins').mkdir(exist_ok=True)
    
    print("Initializing Airflow database...")
    subprocess.run(['airflow', 'db', 'init'], check=True)
    
    print("Creating admin user...")
    subprocess.run([
        'airflow', 'users', 'create',
        '--username', 'admin',
        '--firstname', 'Admin',
        '--lastname', 'User',
        '--role', 'Admin',
        '--email', 'admin@example.com',
        '--password', 'admin'
    ], check=True)
    
    print("Starting Airflow webserver...")
    webserver_process = subprocess.Popen(['airflow', 'webserver', '-D'])
    
    print("Starting Airflow scheduler...")
    scheduler_process = subprocess.Popen(['airflow', 'scheduler', '-D'])
    
    print("Airflow services started successfully!")
    print("Access the UI at: http://localhost:8080")
    print("Username: admin, Password: admin")

if __name__ == "__main__":
    setup_airflow()