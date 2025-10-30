#  MongoDB Ingestion

## 📖 Overview

This part of the project focuses on **loading and cleaning user reviews data** into **MongoDB**.  
It represents the **NoSQL side** of our data pipeline and ensures that all text data is properly prepared for analysis and transformation.

---

## 👩‍💻 Role: MongoDB Engineer

**Responsible for:**

- Setting up MongoDB connection and environment  
- Cleaning and preprocessing the user reviews dataset (`googleplaystore_user_reviews.csv`)  
- Removing **HTML tags**, **emojis**, and unnecessary symbols  
- Loading cleaned data into MongoDB collections  
- Validating data using **MongoDB Compass**

---

## ⚙️ Tech Stack

| Category   | Tools / Libraries               |
|------------|----------------------------------|
| Language   | Python                           |
| Database   | MongoDB                          |
| Libraries  | `pandas`, `beautifulsoup4`, `emoji`, `pymongo` |

---

## 🧰 Project Structure

```
mongodb_ingestion/
│
├── ingest_mongodb.py      # Cleans emojis, HTML, and unwanted symbols then Loads cleaned data into MongoDB
└── README.md              # (this file)
```

---

## 🚀 How to Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure MongoDB is running** locally (or configure an Atlas connection string).

3. **Run the script**:
   ```bash
   python ingest_mongodb.py
   ```
4. **Validate in MongoDB Compass**:  
   Open Compass → Connect to your database → Confirm that the `app_reviews` collection contains cleaned reviews.

---

## 📦 Output

- A **cleaned and structured** `app_reviews` collection in MongoDB  
- Text fields ready for **sentiment analysis** and **dashboard visualization**
