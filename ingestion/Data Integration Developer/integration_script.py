import pandas as pd

# Load datasets from GitHub (CSV + JSON)
apps_df = pd.read_csv("data\\raw\\googleplaystore.csv")
reviews_df = pd.read_json("data\processed\cleaned_user_reviews.json")

# Merge both datasets
merged_df = pd.merge(apps_df, reviews_df, on="App", how="inner")

# Save merged dataset
merged_df.to_csv("data\processed\integrated_data.csv", index=False)

print("Integration complete! Merged file saved in folder.")
