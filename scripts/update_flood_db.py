import logging
from datetime import date
from pathlib import Path

import pandas as pd

from gdacs_flood_db.logger import setup_logging
from gdacs_flood_db.pipeline import download_all_floods
from gdacs_flood_db.utils.detect_db_change import detect_updated_events
from gdacs_flood_db.config import OUTPUT_CSV as NEW_DB_PATH

# --------------------------------------------------
# Configuration
# --------------------------------------------------

LOGGER_NAME = "gdacs.daily_updater"
logger = logging.getLogger(LOGGER_NAME)

setup_logging()


DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
today = date.today()
today_str = today.strftime("%Y%m%d")
LATEST_DB_PATH = DATA_DIR / "latest_gdacs_flood_db.csv"

# --------------------------------------------------
# Helpers
# --------------------------------------------------


def summarize_events(df: pd.DataFrame, max_rows: int = 10) -> str:
    """
    Create a human-readable summary for logging / email.
    Assumes GDACS_ID is the index.
    """
    if df.empty:
        return "None"

    cols = ["country", "fromdate", "todate", "alertlevel"]
    available = [c for c in cols if c in df.columns]

    return df[available].head(max_rows).reset_index().to_string(index=False)


# --------------------------------------------------
# Pipeline
# --------------------------------------------------


def main() -> None:
    logger.info("=" * 70)
    logger.info(f"GDACS Daily Flood DB Update: {today_str}")
    logger.info("=" * 70)

    # ------------------ Download ------------------ #
    logger.info("Downloading latest GDACS flood database...")
    download_all_floods()
    logger.info("Download completed.")

    # ------------------ Load ------------------ #
    if not LATEST_DB_PATH.exists():
        logger.warning("No existing latest DB found. Initializing baseline.")
        # exit early
        df_new = pd.read_csv(NEW_DB_PATH)
        df_new.to_csv(LATEST_DB_PATH)
        logger.info(f"Latest DB initialized: {LATEST_DB_PATH}")
        return
    else:
        df_old = pd.read_csv(LATEST_DB_PATH)

    df_new = pd.read_csv(NEW_DB_PATH)

    logger.info(f"Previous DB size: {len(df_old)} events")
    logger.info(f"New DB size: {len(df_new)} events")

    db_changed = False

    # ------------------ New Events ------------------ #

    new_events = df_new.loc[~df_new["GDACS_ID"].isin(df_old["GDACS_ID"])]

    logger.info(f"New events detected: {len(new_events)}")

    if not new_events.empty:
        logger.info("New events summary:" + summarize_events(new_events))
        db_changed = True

    # ------------------ Changed Events ------------------ #
    if not df_old.empty:
        changed_events = detect_updated_events(df_new, df_old)
    else:
        changed_events = pd.DataFrame()

    logger.info(f"Changed existing events: {len(changed_events)}")

    if not changed_events.empty:
        logger.info("Changed events summary:" + summarize_events(changed_events))

        logger.info(
            "Changed fields per event:"
            + changed_events[["changed_fields"]].reset_index().to_string(index=False)
        )

        db_changed = True

    # ------------------ Persist ------------------ #
    if db_changed:
        df_new.to_csv(LATEST_DB_PATH)
        logger.info(f"Latest DB updated: {LATEST_DB_PATH}")
    else:
        logger.info("No changes detected. Latest DB not updated.")

    # ------------------ Final ------------------ #
    logger.info("=" * 70)
    logger.info("Daily update completed successfully.")
    logger.info("=" * 70)


# --------------------------------------------------
# Entrypoint
# --------------------------------------------------

if __name__ == "__main__":
    main()
