# airflow_config.py

import os
from pathlib import Path

# Airflow home directory
AIRFLOW_HOME = Path.home() / 'airflow'

# Create necessary directories
(AIRFLOW_HOME / 'dags').mkdir(exist_ok=True)
(AIRFLOW_HOME / 'logs').mkdir(exist_ok=True)
(AIRFLOW_HOME / 'plugins').mkdir(exist_ok=True)

# Environment variables for your data sources
ENV_VARS = {
    'MYSQL_HOST': 'localhost',
    'MYSQL_PORT': '3306',
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': 'password',
    'MYSQL_DATABASE': 'playstore_analytics',
    
    'MONGO_HOST': 'localhost',
    'MONGO_PORT': '27017',
    'MONGO_DATABASE': 'playstore_reviews',
    
    'DUCKDB_PATH': '/tmp/app_analytics.duckdb',
    
    'DBT_PROJECT_DIR': '/path/to/your/dbt/project'
}

# Create .env file
env_content = '\n'.join([f'{k}={v}' for k, v in ENV_VARS.items()])

with open(AIRFLOW_HOME / '.env', 'w') as f:
    f.write(env_content)

print("Airflow configuration created successfully!")
print(f"Airflow home: {AIRFLOW_HOME}")
print("Environment variables set in .env file")