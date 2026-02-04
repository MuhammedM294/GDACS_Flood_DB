import pandas as pd
import logging
from pathlib import Path
from gdacs_flood_db.utils.geo_validation import validate_db
from gdacs_flood_db.logger import setup_logging

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"

    db_path = data_dir / "gdacs_flood_db_20260101.csv"
    review_df = validate_db(db_path, logger)
    if review_df is not None:
        print("Events needing review:")
        print(review_df)
    else:
        print("No events need review.")


if __name__ == "__main__":
    main()
