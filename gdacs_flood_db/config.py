from pathlib import Path
from datetime import date


ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

today = date.today()
today_str = today.strftime("%Y%m%d")
OUTPUT_CSV = DATA_DIR / "gdacs_daily_download" / f"gdacs_flood_db_{today_str}.csv"


BASE_URL = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"
