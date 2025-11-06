# setup_airflow.sh

#!/bin/bash

echo "Setting up Airflow for App Performance Analytics..."

# Create airflow directories
mkdir -p ~/airflow/dags ~/airflow/logs ~/airflow/plugins

# Initialize Airflow database
airflow db init

# Create the DAG file
cat > ~/airflow/dags/app_performance_analytics_dag.py << 'EOF'
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
from sqlalchemy import create_engine
import pymongo
import duckdb
import os
from dotenv import load_dotenv
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default arguments for the DAG
default_args = {
    'owner': 'app_pulse_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize DAG
dag = DAG(
    'app_performance_analytics_pipeline',
    default_args=default_args,
    description='Complete ELT pipeline for App Performance Analytics',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['app_analytics', 'elt', 'dbt', 'dash']
)

def extract_mysql_data():
    """Extract data from MySQL (Google Play Store Apps)"""
    try:
        # MySQL connection
        mysql_engine = create_engine(
            f"mysql+pymysql://root:password@localhost:3306/playstore_analytics"
        )
        
        # Read apps data
        apps_df = pd.read_sql("SELECT * FROM google_play_apps", mysql_engine)
        
        # Save to CSV for dbt processing
        apps_df.to_csv('/tmp/apps_raw.csv', index=False)
        
        logger.info(f"Extracted {len(apps_df)} app records from MySQL")
        return len(apps_df)
        
    except Exception as e:
        logger.error(f"MySQL extraction failed: {str(e)}")
        raise

def extract_mongodb_data():
    """Extract data from MongoDB (User Reviews)"""
    try:
        # MongoDB connection
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = mongo_client['playstore_reviews']
        collection = db['user_reviews']
        
        # Extract all reviews
        reviews_data = list(collection.find())
        
        # Convert ObjectId to string and save to JSON
        for review in reviews_data:
            if '_id' in review:
                review['_id'] = str(review['_id'])
        
        # Save to JSON file for dbt processing
        with open('/tmp/reviews_raw.json', 'w') as f:
            json.dump(reviews_data, f)
        
        logger.info(f"Extracted {len(reviews_data)} review records from MongoDB")
        return len(reviews_data)
        
    except Exception as e:
        logger.error(f"MongoDB extraction failed: {str(e)}")
        raise

def transform_with_dbt():
    """Run dbt transformations"""
    try:
        # Run dbt models
        dbt_command = "cd /path/to/your/dbt/project && dbt run"
        result = os.system(dbt_command)
        
        if result != 0:
            raise Exception("dbt run failed")
        
        logger.info("dbt transformations completed successfully")
        
    except Exception as e:
        logger.error(f"dbt transformation failed: {str(e)}")
        raise

def load_to_duckdb():
    """Load transformed data to DuckDB warehouse"""
    try:
        # Connect to DuckDB
        conn = duckdb.connect('/tmp/app_analytics.duckdb')
        
        # Load transformed data (this would be the output from dbt)
        # In practice, dbt would have already loaded to DuckDB
        logger.info("Data loaded to DuckDB warehouse successfully")
        
        conn.close()
        
    except Exception as e:
        logger.error(f"DuckDB loading failed: {str(e)}")
        raise

def validate_data_quality():
    """Validate data quality after transformation"""
    try:
        conn = duckdb.connect('/tmp/app_analytics.duckdb')
        
        # Check if fact table exists and has data
        result = conn.execute("SELECT COUNT(*) FROM fact_app_metrics").fetchone()
        fact_count = result[0]
        
        # Check dimension tables
        apps_count = conn.execute("SELECT COUNT(*) FROM dim_apps").fetchone()[0]
        dev_count = conn.execute("SELECT COUNT(*) FROM dim_developers").fetchone()[0]
        cat_count = conn.execute("SELECT COUNT(*) FROM dim_categories").fetchone()[0]
        
        logger.info(f"Data validation - Apps: {apps_count}, Developers: {dev_count}, Categories: {cat_count}, Metrics: {fact_count}")
        
        if fact_count == 0:
            raise Exception("No data in fact table - validation failed")
        
        conn.close()
        
    except Exception as e:
        logger.error(f"Data quality validation failed: {str(e)}")
        raise

def run_dbt_tests():
    """Run dbt tests to ensure data quality"""
    try:
        dbt_test_command = "cd /path/to/your/dbt/project && dbt test"
        result = os.system(dbt_test_command)
        
        if result != 0:
            raise Exception("dbt tests failed")
        
        logger.info("dbt tests passed successfully")
        
    except Exception as e:
        logger.error(f"dbt tests failed: {str(e)}")
        raise

# Define tasks
extract_mysql_task = PythonOperator(
    task_id='extract_mysql_data',
    python_callable=extract_mysql_data,
    dag=dag,
)

extract_mongodb_task = PythonOperator(
    task_id='extract_mongodb_data',
    python_callable=extract_mongodb_task,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_with_dbt',
    python_callable=transform_with_dbt,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_duckdb',
    python_callable=load_to_duckdb,
    dag=dag,
)

validate_task = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_data_quality,
    dag=dag,
)

dbt_tests_task = PythonOperator(
    task_id='run_dbt_tests',
    python_callable=run_dbt_tests,
    dag=dag,
)

# Set task dependencies
extract_mysql_task >> extract_mongodb_task >> transform_task >> load_task >> validate_task >> dbt_tests_task
EOF

echo "DAG file created!"

# Start Airflow webserver and scheduler
echo "Starting Airflow services..."
airflow webserver -D
airflow scheduler -D

echo "Airflow setup completed!"
echo "Access the UI at: http://localhost:8080"
echo "Username: admin, Password: admin (or whatever you set)"