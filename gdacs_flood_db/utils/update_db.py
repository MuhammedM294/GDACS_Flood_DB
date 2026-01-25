
from pathlib import Path
import pandas as pd
import logging

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent.parent.parent / "data"

RAW_DB_PATH = DATA_DIR / "gdacs_flood_db.csv"
OVERRIDES_PATH = DATA_DIR / "validation_overrides.csv"
OUTPUT_PATH = DATA_DIR / "gdacs_flood_db_corrected.csv"

OVERRIDE_COLUMNS = {
    "Country": "country",
    "Continent": "continent",
    "ISO3": "iso3",
}

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def load_data():
    raw = pd.read_csv(RAW_DB_PATH)
    overrides = pd.read_csv(OVERRIDES_PATH)
    return raw, overrides


def filter_valid_overrides(overrides: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only rows that actually contain at least one correction.
    """
    return overrides.dropna(
        how="all",
        subset=list(OVERRIDE_COLUMNS.keys())
    )


def apply_overrides(raw: pd.DataFrame, overrides: pd.DataFrame) -> pd.DataFrame:
    """
    Apply overrides to the raw database using GDACS_ID as key.
    """
    merged = raw.merge(
        overrides,
        on="GDACS_ID",
        how="left",
        suffixes=("", "_override")
    )

    for override_col, target_col in OVERRIDE_COLUMNS.items():
        merged[target_col] = merged[override_col].combine_first(
            merged[target_col]
        )

    # Keep lon/lat continent consistent if continent is overridden
    if "Continent" in merged.columns:
        merged["continent_lonlat"] = merged["Continent"].combine_first(
            merged["continent_lonlat"]
        )

    # Drop override helper columns
    merged = merged.drop(columns=list(OVERRIDE_COLUMNS.keys()))

    return merged


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    raw_db, overrides = load_data()
    overrides = filter_valid_overrides(overrides)

    corrected_db = apply_overrides(raw_db, overrides)

    corrected_db.to_csv(OUTPUT_PATH, index=False)

    logger.info(f"Corrected database written to: {OUTPUT_PATH}")
    logger.info(f"Total events: {len(corrected_db)}")
    logger.info(f"Corrected events applied: {len(overrides)}")


# if __name__ == "__main__":
#     main()

