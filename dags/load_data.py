from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import pandas as pd
from sqlalchemy import create_engine

def load_data():
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
    reviews_df.to_sql("reviews_raw", con=engine, if_exists="replace", index=False)

with DAG(dag_id="load_playstore_data",
         start_date=datetime(2025,10,29),
         schedule="@daily",
         catchup=False) as dag:

    task_load = PythonOperator(
        task_id="load_csv_to_mysql",
        python_callable=load_data,
        retries=3,
        retry_delay=timedelta(seconds=10)
    )

