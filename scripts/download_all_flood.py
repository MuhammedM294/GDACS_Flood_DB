from gdacs_flood_db.pipeline import download_all_floods
from gdacs_flood_db.logger import setup_logging

if __name__ == "__main__":
    setup_logging()
    total = download_all_floods()
    print(f"Flood events downloaded/updated")


