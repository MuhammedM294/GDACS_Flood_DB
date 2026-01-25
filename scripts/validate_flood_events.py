import pandas as pd
import logging
from pathlib import Path
from gdacs_flood_db.utils.geo_validation import validate_row
from gdacs_flood_db.logger import setup_logging

logger = logging.getLogger(__name__)

def main():
    setup_logging()
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"

    database_path = data_dir / "gdacs_flood_db.csv"
    needs_review_path = data_dir / "needs_review.csv"
    review_work_path = data_dir / "review_work.csv"
    OVERRIDES_PATH = data_dir / "validation_overrides.csv"

    # Load database
    df = pd.read_csv(database_path)
    logger.info(f"Total events: {len(df)}")

    # Detect events needing review
    df["validation_errors"] = df.apply(validate_row, axis=1)
    review_df = df[df["validation_errors"].str.len() > 0].copy()

    logger.info(f"Events needing review: {len(review_df)}")

    # Save full rows for traceability
    review_df.to_csv(needs_review_path, index=False)

    # Save human-friendly subset
    review_cols = [
        "GDACS_ID",
        "validation_errors",
        "country",
        "country_lonlat",
        "continent",
        "continent_lonlat",
        "fromdate",
        "todate",
        "geometry_url",
        "alertlevel",
    ]

    review_df[review_cols].to_csv(review_work_path, index=False)

    logger.info(f"Saved: {needs_review_path}")
    logger.info(f"Saved: {review_work_path}")

    


    if not review_df.empty:
        override_template = review_df[[
                    "GDACS_ID",
                    "continent",
                    "country",
                    "iso3",
                ]].copy()

        override_template.rename(columns={
            "country": "original_country",
            "continent": "original_continent",
        }, inplace=True)

        override_template["corrected_continent"] = ""
        override_template["reason"] = ""
        override_template["source"] = ""
        override_template["reviewed_by"] = ""
        override_template["reviewed_at"] = ""

        override_template.to_csv(
            OVERRIDES_PATH,
            index=False
        )
        logger.info(f"Created override file at: {OVERRIDES_PATH}")

    

if __name__ == "__main__":
    main()
