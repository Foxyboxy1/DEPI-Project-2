
# 🗃️ MySQL Ingestion – Member 1

This module loads the **Google Play Store Apps dataset** (`googleplaystore.csv`) into a MySQL database as part of the playstore ELT pipeline.

## 📥 Input Source
- File: `data/raw/googleplaystore.csv`  
  (Download from [Kaggle: Google Play Store Apps](https://www.kaggle.com/datasets/lava18/google-play-store-apps))

## 🗄️ Output Destination
- **Database**: `playstore`  
- **Table**: `play_store_apps`

### Table Schema
| Column | Type | Description |
|--------|------|-------------|
| `app` | `VARCHAR(255)` | App name (e.g., "WhatsApp Messenger") |
| `category` | `VARCHAR(100)` | App category (e.g., "COMMUNICATION") |
| `rating` | `DECIMAL(3,1)` | Average rating (1–5) |
| `reviews` | `INT` | Total number of reviews |
| `size` | `VARCHAR(20)` | App size (e.g., "3.5M") |
| `installs` | `VARCHAR(50)` | Install range (e.g., "10,000+") |
| `type` | `VARCHAR(20)` | "Free" or "Paid" |
| `price` | `VARCHAR(20)` | Price string (e.g., "0", "$4.99") |
| `content_rating` | `VARCHAR(50)` | Content rating (e.g., "Everyone") |
| `genres` | `VARCHAR(255)` | Genres (e.g., "Art & Design") |
| `last_updated` | `DATE` | Last update date |
| `current_ver` | `VARCHAR(50)` | Current version |
| `android_ver` | `VARCHAR(50)` | Android version requirement |

> 🔑 **Key field**: `app` is preserved exactly as in the source to enable joining with MongoDB reviews later.

## ⚙️ Setup & Execution

### Prerequisites
- MySQL 8.0+ running locally
- Python 3.9+

### 1. Configure Environment
Copy the example file and fill in your credentials:
```bash
cp .env.example .env
```

Example `.env`:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=apppulse
```

### 2. Create Database & Table
Run the schema script in MySQL:
```sql
source ingestion/mysql_ingestion/schema.sql;
```

### 3. Run Ingestion Script
```bash
python ingestion/mysql_ingestion/ingest_mysql.py
```

### ✅ Expected Output
```
✅ Loaded 10841 rows from CSV.
✅ Connected to MySQL
✅ Successfully inserted 10841 rows into MySQL.
🔍 Sample rows: [...]
🔒 MySQL connection closed.
```

## 🔄 Data Notes
- Minimal cleaning only (numbers → numeric, dates → DATE)
- No transformation of `installs`, `price`, or `size` — this is handled in the **dbt layer**
- Malformed CSV lines are skipped (`on_bad_lines='skip'`)