import pandas as pd
import os

# Load datasets from GitHub (CSV + JSON)
apps_df = pd.read_csv("/app/data/raw/googleplaystore.csv")
reviews_df = pd.read_csv("/app/data/raw/googleplaystore_user_reviews.csv")

# Merge both datasets
merged_df = pd.merge(apps_df, reviews_df, on="App", how="inner")

# Output path
output_path = os.getenv("OUTPUT_PATH", "data/integrated_data.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save merged dataset
merged_df.to_csv(output_path, index=False)

print("Integration complete! Merged file saved in folder:", output_path)
