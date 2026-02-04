from datetime import date
from .equi7_grid_code import get_equ7_code_lonlat


def month_windows(start: date, end: date):
    """
    Yield (start, end) monthly windows.

    """
    current = start
    while current < end:
        if current.month == 12:
            nxt = date(current.year + 1, 1, 1)
        else:
            nxt = date(current.year, current.month + 1, 1)

        yield current, min(nxt, end)
        current = nxt


def resolve_country_from_gdacs(props: dict) -> dict | None:
    affected = props.get("affectedcountries")

    if isinstance(affected, list) and affected:
        c = affected[0] or {}
        return {
            "country_name": c.get("countryname"),
            "iso2": c.get("iso2"),
            "iso3": c.get("iso3"),
            "source": "gdacs",
        }

    if props.get("country"):
        return {
            "country_name": props.get("country"),
            "iso2": None,
            "iso3": None,
            "source": "gdacs",
        }

    return None


def normalize_flood_event(feature: dict) -> dict:
    props = feature.get("properties", {})
    geom = feature.get("geometry", {})
    lon, lat = geom.get("coordinates", (None, None))

    # Primary source: GDACS
    country_gdacs = resolve_country_from_gdacs(props)

    # add Equi7 grid code based on lon/lat
    equi7_code = get_equ7_code_lonlat(lon, lat)

    return {
        "GDACS_ID": f"{props.get('eventtype')}-{props.get('eventid')}",
        "equi7_grid_code": equi7_code,
        # primary (GDACS)
        "country": country_gdacs.get("country_name") if country_gdacs else None,
        "iso3": country_gdacs.get("iso3") if country_gdacs else None,
        # metadata
        "eventid": props.get("eventid"),
        "alertlevel": props.get("alertlevel"),
        "alertscore": props.get("alertscore"),
        "fromdate": props.get("fromdate"),
        "todate": props.get("todate"),
        # urls
        "geometry_url": props.get("url", {}).get("geometry"),
        "report_url": props.get("url", {}).get("report"),
        "details_url": props.get("url", {}).get("details"),
        "geometry": geom,
    }


if __name__ == "__main__":
    pass
