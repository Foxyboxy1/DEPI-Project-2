def extract_for_duckdb(filter_col=None, filter_val=None):
    df = pd.read_csv("integrated_data.csv")
    if filter_col and filter_val:
        df = df[df[filter_col] == filter_val]
    df.to_csv("duckdb_ready.csv", index=False)
