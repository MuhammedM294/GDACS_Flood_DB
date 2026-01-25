from datetime import datetime
from urllib.parse import urlparse, parse_qs
ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"


RULE_MISSING_CONTINENT = "missing_continent"
RULE_MISSING_CONTINENT_LONLAT = "missing_continent_lonlat"
RULE_COUNTRY_MISMATCH = "country_mismatch"
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
    if not row.get("continent"):
        reasons.append(RULE_MISSING_CONTINENT)

    if not row.get("continent_lonlat"):
        reasons.append(RULE_MISSING_CONTINENT_LONLAT)

    if row.get("country") != row.get("country_lonlat"):
        reasons.append(RULE_COUNTRY_MISMATCH)

    # Temporal checks
    if not is_valid_iso_datetime(row.get("fromdate")):
        reasons.append(RULE_INVALID_FROMDATE)

    if not is_valid_iso_datetime(row.get("todate")):
        reasons.append(RULE_INVALID_TODATE)

    # Geometry / AOI checks
    if not is_valid_geometry_url(row.get("geometry_url")):
        reasons.append(RULE_INVALID_GEOMETRY_URL)

    return reasons


