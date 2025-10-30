import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample data
np.random.seed(42)
n = 200

categories = ["COMMUNICATION", "SOCIAL", "TOOLS", "PHOTOGRAPHY", "GAMES", "PRODUCTIVITY"]
apps = [f"App {i}" for i in range(1, n+1)]

sample_df = pd.DataFrame({
    "app": np.random.choice(apps, n),
    "category": np.random.choice(categories, n),
    "avg_rating": np.round(np.random.uniform(3.0, 5.0, n), 1),
    "installs": np.random.choice([1000, 10000, 100000, 1000000, 10000000], n),
    "reviews_count": np.random.randint(50, 50000, n),
    "price": np.random.choice([0.0, 0.99, 2.99, 4.99, 9.99], n),
    "sentiment_score": np.round(np.random.uniform(0.3, 1.0, n), 2),
    "last_updated": [datetime.today() - timedelta(days=np.random.randint(0, 365)) for _ in range(n)]
})

# Save as Parquet (lightweight & fast)
sample_df.to_parquet("visualization/sample_data.parquet", index=False)