from gdacs_flood_db.pipeline import download_all_floods
from gdacs_flood_db.logger import setup_logging

if __name__ == "__main__":
    setup_logging()
    total = download_all_floods()
    print(f"Flood events downloaded/updated")
#     import pandas as pd

#     df = pd.read_csv("/home/m294/repo/gdacs_flood_db/data/gdacs_flood_db.csv")
#     mask_empty_continent = (
#     df["continent"].isna()
#     | (df["continent"].astype(str).str.strip() == "")

# )
#     df_missing_continent = df.loc[mask_empty_continent, ["country", "continent"]]
#     print(df_missing_continent)
#     print(f"Total missing continent: {len(df_missing_continent)}")
#     problem_countries = (
#     df_missing_continent["country"]
#     .dropna()
#     .astype(str)
#     .str.strip()
#     .value_counts()
# )

#     print(problem_countries)

