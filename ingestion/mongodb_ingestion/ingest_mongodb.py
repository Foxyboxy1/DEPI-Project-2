from pymongo import MongoClient

client=MongoClient()

db=client["playstore_reviews"]
collection=db["users_reviews"]

pip install emoji

import bs4 
print('beautiful soup exists')
    
import pandas as pd 
#download data
df=pd.read_csv("googleplaystore_user_reviews.csv")
df.head()
    
import re
import emoji
from bs4 import BeautifulSoup

def clean_text(text):
      
    if not isinstance(text, str):
        text = str(text)    
            
    if "\\" in text or "/" in text or ":" in text:
         text = text.split("\\")[-1]  # ناخد آخر جزء بس
        
    try:
        text = BeautifulSoup(text, "html.parser").get_text()
    except Exception:
        text=text
            
    try:
        text = emoji.replace_emoji(text, replace='')
    except Exception:
        text=text
            
    text = re.sub(r'[^A-Za-z0-9\s.,!?\'\"]+', ' ', text)
    return text.strip()
    
df["Cleaned_Review"]=df["Translated_Review"].apply(clean_text)
print(df[["Translated_Review","Cleaned_Review"]].head())

data_to_insert=df.to_dict("records")
collection.insert_many(data_to_insert)
print("donnne")

from pymongo import MongoClient
import json

client = MongoClient()
db = client["playstore_reviews"]          
collection = db["user_reviews"]           

sample_data = list(collection.find())


for doc in sample_data:
    doc.pop('_id', None)

with open("cleaned_user_reviews_sample.json", "w", encoding="utf-8") as f:
    json.dump(sample_data, f, ensure_ascii=False, indent=2)

print("✅ Sample exported successfully!")
                            
