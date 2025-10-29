import pandas as pd
import re
import emoji
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json

# Load the CSV data
df = pd.read_csv("data\\raw\\googleplaystore_user_reviews.csv")

# Define text cleaning function
def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')
    
    # Keep only letters, digits, spaces, and basic punctuation
    text = re.sub(r'[^A-Za-z0-9\s.,!?\'\"]+', ' ', text)
    
    return text.strip()

# Apply cleaning to the 'Translated_Review' column
df["Cleaned_Review"] = df["Translated_Review"].apply(clean_text)

# Connect to MongoDB and insert data
client = MongoClient()
db = client["playstore_reviews"]
collection = db["user_reviews"]  # Consistent collection name

# Insert all records
collection.insert_many(df.to_dict("records"))
print("✅ Data inserted successfully into MongoDB!")

# Export a sample (or all) documents to JSON (without _id)
sample_data = list(collection.find({}, {"_id": 0}))  # Exclude _id field

with open("cleaned_user_reviews.json", "w", encoding="utf-8") as f:
    json.dump(sample_data, f, ensure_ascii=False, indent=2)

print("✅ Data exported to 'cleaned_user_reviews.json'!")