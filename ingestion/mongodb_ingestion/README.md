Google Play Store Data Engineering Project — MongoDB Ingestion

📖 Overview

This part of the project is focusing on loading and cleaning user reviews data into MongoDB.
It represents the NoSQL side of our data pipeline and ensures that all text data is properly prepared for analysis and transformation.

👩‍💻 Role: MongoDB Engineer

Responsible for:

Setting up MongoDB connection and environment.

Cleaning and preprocessing user reviews dataset (googleplaystore_user_reviews.csv).

Removing HTML tags, emojis, and unnecessary symbols.

Loading cleaned data into MongoDB collections.

Validating data in MongoDB Compass.


---

⚙️ Tech Stack

Category	Tools / Libraries

Language	Python
Database	MongoDB
Libraries	Pandas, BeautifulSoup4, Emoji, PyMongo

---

🧰 Project Structure

mongodb_ingestion/
│
├── clean_text.py          # Cleans emoji + HTML + unwanted symbols
├── load_reviews.py        # Loads cleaned data into MongoDB
├── googleplaystore_user_reviews.csv
└── README.md              # (this file)


---

🚀 How to Run

1. Install dependencies:

pip install -r requirements.txt


2. Make sure MongoDB is running locally (or use Atlas connection string).


3. Run the cleaning script:

python clean_text.py


4. Then load the cleaned dataset to MongoDB:

python load_reviews.py


5. Open MongoDB Compass → check your database → confirm that the cleaned reviews are uploaded.




---

📦 Output

Cleaned and structured user reviews collection in MongoDB.

Text fields ready for sentiment analysis and dashboard visualization.
