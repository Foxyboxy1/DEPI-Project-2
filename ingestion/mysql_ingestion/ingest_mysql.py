import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

def clean_date(date_str):
    if pd.isna(date_str):
        return None
    for fmt in ('%B %d, %Y', '%b %d, %Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(str(date_str), fmt).date()
        except ValueError:
            continue
    return None

def main():
    # 1. Load CSV
    csv_path = "data/raw/googleplaystore.csv"
    df = pd.read_csv(
        csv_path,
        on_bad_lines='skip',
        encoding='utf-8',
        engine='python'
    )
    print(f"✅ Loaded {len(df)} rows from CSV.")

    correct_columns = [
        'app', 'category', 'rating', 'reviews', 'size',
        'installs', 'type', 'price', 'content_rating',
        'genres', 'last_updated', 'current_ver', 'android_ver'
    ]
    if df.shape[1] == 13:
        df.columns = correct_columns
    else:
        raise ValueError(f"Expected 13 columns, but got {df.shape[1]}. Check CSV format.")

    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
    df['last_updated'] = df['last_updated'].apply(clean_date)

    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )

        if connection.is_connected():
            print("✅ Connected to MySQL")
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE play_store_apps;")

            insert_query = """
            INSERT INTO play_store_apps (
                app, category, rating, reviews, size, installs, type,
                price, content_rating, genres, last_updated, current_ver, android_ver
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            data_tuples = [
                (
                    row['app'],
                    row['category'],
                    row['rating'],
                    row['reviews'],
                    row['size'],
                    row['installs'],
                    row['type'],
                    row['price'],
                    row['content_rating'],
                    row['genres'],
                    row['last_updated'],
                    row['current_ver'],
                    row['android_ver']
                )
                for _, row in df.iterrows()
            ]


            cursor.executemany(insert_query, data_tuples)
            connection.commit()
            print(f"✅ Successfully inserted {len(data_tuples)} rows into MySQL.")

            cursor.execute("SELECT app, category, rating FROM play_store_apps LIMIT 3;")
            sample = cursor.fetchall()
            print("🔍 Sample rows:", sample)

    except Error as e:
        print(f"❌ MySQL Error: {e}")
    except Exception as e:
        print(f"❌ General Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    main()