# from gdacs_flood_db.pipeline import download_all_floods
# from gdacs_flood_db.logger import setup_logging

if __name__ == "__main__":
    # setup_logging()
    # total = download_all_floods()
    # print(f"Flood events downloaded/updated")
    import pandas as pd
    from pathlib import Path
    database = Path(__file__).parent.parent / "data" / "gdacs_flood_db.csv"
    df = pd.read_csv(database)
    print(f"Total events: {len(df)}")
    def needs_review(row):
        return (
            row["continent"] is None
            or row["continent_lonlat"] is None
            or row["country"] != row["country_lonlat"]
        )
    df[df.apply(needs_review, axis=1)].to_csv("data/needs_review.csv")
    print(f"Events needing review: {len(df[df.apply(needs_review, axis=1)])}")
    review_cols = [
    "GDACS_ID",
    "country",
    "country_lonlat",
    "continent",
    "continent_lonlat",
    "alertlevel",
    ]
    df[review_cols].to_csv("data/review_work.csv", index=False)

   



