from datetime import date
from .geo_lookup import country_from_lonlat
from .country_resolution import (
    resolve_country_from_gdacs,
    resolve_continent,
)

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




def normalize_flood_event(feature: dict) -> dict:
    props = feature.get("properties", {})
    geom = feature.get("geometry", {})
    lon, lat = geom.get("coordinates", (None, None))

    # Primary source: GDACS
    country_gdacs = resolve_country_from_gdacs(props)
    continent_gdacs = resolve_continent(country_gdacs)

    # Secondary source: lon/lat
    country_ll = country_from_lonlat(lon, lat)
    continent_ll = resolve_continent(country_ll)

    return {
        "GDACS_ID": f"{props.get('eventtype')}-{props.get('eventid')}",

        # primary (GDACS)
        "country": country_gdacs.get("country_name") if country_gdacs else None,
        "iso3": country_gdacs.get("iso3") if country_gdacs else None,
        "continent": continent_gdacs,

        # secondary (lon/lat)
        "country_lonlat": country_ll.get("country_name") if country_ll else None,
        "iso3_lonlat": country_ll.get("iso3") if country_ll else None,
        "continent_lonlat": continent_ll,

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