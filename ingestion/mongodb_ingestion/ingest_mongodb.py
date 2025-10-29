# -------------------------------
# 1. IMPORTS & SETUP
# -------------------------------
from pymongo import MongoClient
import pandas as pd
import re
import emoji
from bs4 import BeautifulSoup
import json

print("✅ All libraries imported successfully!")

# -------------------------------
# 2. CONNECT TO MONGODB
# -------------------------------
client = MongoClient("mongodb://localhost:27017/")  
db = client["playstore_reviews"]
collection = db["user_reviews"]

# -------------------------------
# 3. LOAD RAW DATA
# -------------------------------
print("📥 Loading dataset...")
df = pd.read_csv("data\raw\googleplaystore_user_reviews.csv")

# -------------------------------
# 4. CLEAN FUNCTION
# -------------------------------
def clean_text(text):
    if not isinstance(text, str):
        text = str(text)

    # إزالة المسارات
    if "\\" in text or "/" in text or ":" in text:
        text = text.split("\\")[-1]

    # إزالة HTML tags
    try:
        text = BeautifulSoup(text, "html.parser").get_text()
    except Exception:
        pass

    # إزالة الرموز التعبيرية
    try:
        text = emoji.replace_emoji(text, replace="")
    except Exception:
        pass

    # إزالة الرموز الغريبة
    text = re.sub(r"[^A-Za-z0-9\s.,!?'\"]+", " ", text)

    return text.strip()

# -------------------------------
# 5. APPLY CLEANING
# -------------------------------
print("🧹 Cleaning text...")
df["Cleaned_Review"] = df["Translated_Review"].apply(clean_text)

# -------------------------------
# 6. INSERT INTO MONGODB
# -------------------------------
print("📤 Inserting data into MongoDB...")
data_to_insert = df.to_dict("records")
collection.insert_many(data_to_insert)
print(f"✅ Inserted {len(data_to_insert)} records into MongoDB")

# -------------------------------
# 7. EXPORT CLEANED SAMPLE TO JSON
# -------------------------------
print("💾 Exporting cleaned data to JSON...")

# نقرأ من قاعدة البيانات بعد الإدخال
sample_data = list(collection.find({}, {"_id": 0}))  # إزالة الـ _id تلقائيًا

with open("cleaned_user_reviews.json", "w", encoding="utf-8") as f:
    json.dump(sample_data, f, ensure_ascii=False, indent=2)

print("🎉 cleaned_user_reviews.json exported successfully!")
