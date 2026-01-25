from pathlib import Path
import pandas as pd
import requests
import json
import time

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent.parent.parent / "data"
DB_PATH = DATA_DIR / "gdacs_flood_db_corrected.csv"
AOI_DIR = DATA_DIR / "aois"

REQUEST_TIMEOUT = 30  # seconds
SLEEP_BETWEEN_REQUESTS = 0.5  

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def ensure_aoi_dir():
    AOI_DIR.mkdir(parents=True, exist_ok=True)


def load_database() -> pd.DataFrame:
    return pd.read_csv(DB_PATH)


def download_aoi(url: str) -> dict:
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def save_aoi(gdacs_id: str, data: dict):
    output_path = AOI_DIR / f"{gdacs_id}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# -----------------------------------------------------------------------------
# Main logic
# -----------------------------------------------------------------------------

def main():
    ensure_aoi_dir()
    df = load_database()

    total = len(df)
    downloaded = 0
    skipped = 0
    failed = 0

    for _, row in df.iterrows():
        gdacs_id = row.get("GDACS_ID")
        geometry_url = row.get("geometry_url")

        if not gdacs_id or not geometry_url:
            failed += 1
            continue

        output_file = AOI_DIR / f"{gdacs_id}.json"

        if output_file.exists():
            skipped += 1
            continue

        try:
            aoi_data = download_aoi(geometry_url)
            save_aoi(gdacs_id, aoi_data)
            downloaded += 1
            time.sleep(SLEEP_BETWEEN_REQUESTS)

        except Exception as e:
            print(f"[ERROR] {gdacs_id}: {e}")
            failed += 1

    print("AOI download summary")
    print("--------------------")
    print(f"Total events     : {total}")
    print(f"Downloaded       : {downloaded}")
    print(f"Already existed  : {skipped}")
    print(f"Failed           : {failed}")


if __name__ == "__main__":
    main()
