from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_CSV = DATA_DIR / "gdacs_flood_db.csv"

BASE_URL = (
    "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"
)




