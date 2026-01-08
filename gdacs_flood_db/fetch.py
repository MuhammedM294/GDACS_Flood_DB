from .config import BASE_URL

def fetch_window(session, start, end, retries=3, timeout=30):
    params = {
        "eventlist": "FL",
        "fromdate": start.isoformat(),
        "todate": end.isoformat(),
        "alertlevel": "green;orange;red",
    }

    for attempt in range(1, retries + 1):
        r = session.get(BASE_URL, params=params, timeout=timeout)

        if r.status_code != 200:
            print(f"HTTP {r.status_code} for {start} → {end} (attempt {attempt})")
            continue

        try:
            payload = r.json()
            return payload.get("features", [])
        except ValueError:
            print(f"Invalid JSON for {start} → {end} (attempt {attempt})")

    print(f"Skipping window {start} → {end} after {retries} failures")
    return []
