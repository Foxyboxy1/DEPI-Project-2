# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime,timedelta
# import pandas as pd
# from sqlalchemy import create_engine

# def load_data():
#     engine = create_engine("mysql+pymysql://root:root@mysql:3306/playstore")
#     apps_df = pd.read_csv("/app/data/raw/googleplaystore.csv")
#     reviews_df = pd.read_csv("/app/data/raw/googleplaystore_user_reviews.csv")

#     apps_df.to_sql("apps_raw", con=engine, if_exists="replace", index=False)
#     reviews_df.rename(columns={
#         'App': 'app_id',
#         'Translated_Review': 'translated_review',
#         'Sentiment': 'sentiment',
#         'Sentiment_Polarity': 'sentiment_polarity',
#         'Sentiment_Subjectivity': 'sentiment_subjectivity'
#     }, inplace=True)
#     reviews_df.to_sql("reviews_raw", con=engine, if_exists="replace", index=False)

# with DAG(dag_id="load_playstore_data",
#          start_date=datetime(2025,10,29),
#          schedule="@daily",
#          catchup=False) as dag:

#     task_load = PythonOperator(
#         task_id="load_csv_to_mysql",
#         python_callable=load_data,
#         retries=3,
#         retry_delay=timedelta(seconds=10)
#     )



from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

def load_raw_data():
    """Load raw data to MySQL"""
    engine = create_engine("mysql+pymysql://root:root@mysql:3306/playstore")
    
    apps_df = pd.read_csv("/app/data/raw/googleplaystore.csv")
    reviews_df = pd.read_csv("/app/data/raw/googleplaystore_user_reviews.csv")

    apps_df.to_sql("apps_raw", con=engine, if_exists="replace", index=False)
    
    reviews_df.rename(columns={
        'App': 'app_id',
        'Translated_Review': 'translated_review',
        'Sentiment': 'sentiment',
        'Sentiment_Polarity': 'sentiment_polarity',
        'Sentiment_Subjectivity': 'sentiment_subjectivity'
    }, inplace=True)
    
    reviews_df.to_sql("user_reviews_raw", con=engine, if_exists="replace", index=False)
    
    print(f"✅ Loaded {len(apps_df)} apps and {len(reviews_df)} reviews")

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="playstore_star_schema_etl",
    default_args=default_args,
    description='Star Schema ETL pipeline for Play Store data',
    schedule_interval="@daily",
    start_date=datetime(2025, 10, 29),
    catchup=False,
    tags=['playstore', 'star-schema', 'dbt'],
) as dag:

    load_data = PythonOperator(
        task_id="load_raw_data",
        python_callable=load_raw_data,
    )

    dbt_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command="cd /app/dbt_project && dbt run --models staging",
    )

    dbt_dimensions = BashOperator(
        task_id="dbt_run_dimensions",
        bash_command="cd /app/dbt_project && dbt run --models dim_app dim_category dim_date",
    )

    dbt_facts = BashOperator(
        task_id="dbt_run_facts",
        bash_command="cd /app/dbt_project && dbt run --models fact_app_metrics",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /app/dbt_project && dbt test",
    )

    # Pipeline flow
    load_data >> dbt_staging >> dbt_dimensions >> dbt_facts >> dbt_test