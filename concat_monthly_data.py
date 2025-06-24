import polars as pl



import glob

dfs = []

for filepath in glob.glob("MonthlyData/*.csv"):
    df = pl.read_csv(filepath)

    # Rename columns if needed
    col_map = {
        "Measurement Time": "Time",
        "Production (Wh)": "System Production (Wh)"
    }
    df = df.rename({k: v for k, v in col_map.items() if k in df.columns})

    # Continue only if required columns are present
    if "Time" in df.columns and "System Production (Wh)" in df.columns:
        df = df.select([
            pl.col("Time").str.strptime(pl.Date, "%m/%d/%Y", strict=False).alias("Time"),
            (pl.col("System Production (Wh)") / 1000).alias("Production")
        ])
        dfs.append(df)

# Concatenate and sort all data
if dfs:
    combined = pl.concat(dfs).sort("Time")
    combined.write_csv("solar_production.csv")
else:
    print("No valid files found.")