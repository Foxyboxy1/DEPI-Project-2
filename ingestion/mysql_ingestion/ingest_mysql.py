import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def clean_date(date_str):
    """Try to parse multiple date formats safely."""
    if pd.isna(date_str):
        return None
    for fmt in ('%B %d, %Y', '%b %d, %Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(str(date_str), fmt).date()
        except ValueError:
            continue
    return None


def main():
    # 1️⃣ Load CSV
    csv_path = "data/raw/googleplaystore.csv"
    df = pd.read_csv(csv_path, on_bad_lines='skip', encoding='utf-8', engine='python')
    print(f"✅ Loaded {len(df)} rows from CSV.")

    # 2️⃣ Rename columns
    correct_columns = [
        'app', 'category', 'rating', 'reviews', 'size',
        'installs', 'type', 'price', 'content_rating',
        'genres', 'last_updated', 'current_ver', 'android_ver'
    ]
    if df.shape[1] == 13:
        df.columns = correct_columns
    else:
        raise ValueError(f"Expected 13 columns, but got {df.shape[1]}")

    # 3️⃣ Clean & convert
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
    df['last_updated'] = df['last_updated'].apply(clean_date)

    # Remove +, , etc. from installs
    df['installs'] = df['installs'].astype(str).str.replace('[^0-9]', '', regex=True)
    df['installs'] = pd.to_numeric(df['installs'], errors='coerce')

    # Strip spaces from strings
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # 🔧 Replace any remaining "nan" or "None" text with None
    df = df.replace(['nan', 'NaN', 'None', 'NULL', 'null', 'NAN'], None)
    df = df.where(pd.notnull(df), None)

    print("🔍 Data sample before insert:")
    print(df.head(3))

    # 4️⃣ Connect to MySQL
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

            import numpy as np

            data_tuples = []
            for _, row in df.iterrows():
                clean_row = []
                for val in row:
                    if pd.isna(val) or val in ["nan", "NaN", "None", "NULL", "null"]:
                        clean_row.append(None)
                    elif isinstance(val, (np.generic,)):  # convert numpy types to Python
                        clean_row.append(val.item())
                    else:
                        clean_row.append(val)
                data_tuples.append(tuple(clean_row))


            cursor.executemany(insert_query, data_tuples)
            connection.commit()

            print(f"✅ Inserted {len(data_tuples)} rows successfully.")

            cursor.execute("SELECT app, category, rating FROM play_store_apps LIMIT 3;")
            print("🔍 Sample rows:", cursor.fetchall())

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
