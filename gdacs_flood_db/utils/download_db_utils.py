from datetime import date


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
    """
    Normalize a GDACS flood event feature into a flat dictionary.
    """
    bbox = feature.get("bbox", [])
    location = feature.get("geometry", {})
    props = feature.get("properties", {})
    urls = props.get("url") or {}

    return {
        "GDACS_ID": f"{props.get('eventtype')}-{props.get('eventid')}",
        "eventid": props.get("eventid"),
        "eventtype": props.get("eventtype"),
        "glide": props.get("glide"),
        "alertlevel": props.get("alertlevel"),
        "alertscore": props.get("alertscore"),
        "episodealertlevel": props.get("episodealertlevel"),
        "episodealertscore": props.get("episodealertscore"),
        "country": props.get("country"),
        "fromdate": props.get("fromdate"),
        "todate": props.get("todate"),
        "datemodified": props.get("datemodified"),
        "source": props.get("source"),
        "affectedcountries": props.get("affectedcountries"),
        "geometry_url": urls.get("geometry"),
        "report_url": urls.get("report"),
        "details_url": urls.get("details"),
        "bbox": bbox,
        "location_type": location.get("type"),
        "location_coordinates": location.get("coordinates"),
    }

if __name__ == "__main__":
    for start, end in month_windows(date(2020, 1, 15), date(2024, 5, 10)):
        print(f"From {start} to {end}")