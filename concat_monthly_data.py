import polars as pl

q = (
    pl.scan_csv("MonthlyData/*.csv", try_parse_dates=True)
    .select(
            # Convert the Time column to a proper date
            pl.col("Time")
            .str.strptime(pl.Date, format="%m/%d/%Y")
            .alias("Time"),
            # Divide by 1000 and alias as kWh for clarity
            (pl.col("System Production (Wh)") / 1000)
            .alias("Production"),
    
        )
        .sort("Time")

)

df=q.collect()

df.write_csv('solar_production.csv')