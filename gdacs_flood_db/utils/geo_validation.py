from datetime import datetime
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import pandas as pd

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"

RULE_INVLAID_EQUI7_GRID_CODE = "invalid_equi7_grid_code"
RULE_INVALID_FROMDATE = "invalid_fromdate"
RULE_INVALID_TODATE = "invalid_todate"
RULE_INVALID_GEOMETRY_URL = "invalid_geometry_url"


def is_valid_iso_datetime(value: str) -> bool:
    if not value or not isinstance(value, str):
        return False
    try:
        datetime.strptime(value, ISO_FORMAT)
        return True
    except ValueError:
        return False


def is_valid_geometry_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False

    parsed = urlparse(url)

    # Basic URL structure
    if parsed.scheme not in {"http", "https"}:
        return False

    if "gdacs.org" not in parsed.netloc:
        return False

    if not parsed.path.endswith("/getgeometry"):
        return False

    # Query parameters
    params = parse_qs(parsed.query)

    if params.get("eventtype", [None])[0] != "FL":
        return False

    if not params.get("eventid", [None])[0]:
        return False

    if not params.get("episodeid", [None])[0]:
        return False

    return True


def validate_row(row) -> list[str]:
    """
    Validate a single GDACS flood event row.

    Returns:
        List of rule IDs explaining why the row needs manual review.
        Empty list means the row is valid.
    """
    reasons = []

    # Spatial / semantic checks
    if not row.get("equi7_grid_code"):
        reasons.append(RULE_INVLAID_EQUI7_GRID_CODE)

    # Temporal checks
    if not is_valid_iso_datetime(row.get("fromdate")):
        reasons.append(RULE_INVALID_FROMDATE)

    if not is_valid_iso_datetime(row.get("todate")):
        reasons.append(RULE_INVALID_TODATE)

    # Geometry / AOI checks
    if not is_valid_geometry_url(row.get("geometry_url")):
        reasons.append(RULE_INVALID_GEOMETRY_URL)

    return reasons


def derived_db_path(base: Path, suffix: str) -> Path:
    return base.with_name(f"{base.stem}_{suffix}{base.suffix}")


def validate_db(db_path: Path, logger) -> pd.DataFrame:
    """
    Validate the GDACS flood event database.

    """
    # Load database
    df = pd.read_csv(db_path)
    logger.info(f"Total events: {len(df)}")

    # Detect events needing review
    df["validation_errors"] = df.apply(validate_row, axis=1)
    review_df = df[df["validation_errors"].str.len() > 0].copy()

    if review_df is None or len(review_df) == 0:
        logger.info("No events need review.")
        return None
    else:
        logger.info(f"Events needing review: {len(review_df)}")

        NEED_REVIEW_PATH = derived_db_path(db_path, "needs_review")
        REVIEW_WORK_PATH = derived_db_path(db_path, "review_work")

        review_df.to_csv(NEED_REVIEW_PATH, index=False)

        # Save human-friendly subset
        review_cols = [
            "GDACS_ID",
            "validation_errors",
            "equi7_grid_code",
            "country",
            "fromdate",
            "todate",
            "geometry_url",
            "alertlevel",
        ]

        review_df[review_cols].to_csv(REVIEW_WORK_PATH, index=False)

        logger.info(f"Saved: {NEED_REVIEW_PATH}")
        logger.info(f"Saved: {REVIEW_WORK_PATH}")

    return review_df
