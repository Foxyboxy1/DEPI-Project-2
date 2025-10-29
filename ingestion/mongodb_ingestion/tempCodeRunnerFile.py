
with open("cleaned_user_reviews.json", "w", encoding="utf-8") as f:
    json.dump(sample_data, f, ensure_ascii=False, indent=2)

print("🎉 cleaned_user_reviews.json exported successfully!")
