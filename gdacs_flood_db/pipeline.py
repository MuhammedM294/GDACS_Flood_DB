import csv
import requests
from datetime import date
from .config import OUTPUT_CSV
from .fetch import fetch_window
from .utils.download_db_utils import normalize_flood_event , month_windows
from .schema import FLOOD_FIELDS as FIELDS



def download_all_floods(
    start_date: date = date(2015, 1, 1),
    end_date: date | None = None,
):
    if end_date is None:
        end_date = date.today()

    seen = set()
    total = 0

    with requests.Session() as session, OUTPUT_CSV.open(
        "w", newline="", encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()

        for win_start, win_end in month_windows(start_date, end_date):
            events = fetch_window(session, win_start, win_end)

            if len(events) == 100:
                print(
                    f"WARNING: {win_start}–{win_end} returned 100 events "
                    "(unexpected for monthly window)"
                )

            for feature in events:
                event_id = feature.get("properties", {}).get("eventid")

                if event_id in seen:
                    continue

                seen.add(event_id)
                writer.writerow(normalize_flood_event(feature))
                total += 1

            print(f"✔ {win_start} → {win_end}: {len(events)} events")

    print(f"\n Finished: {total} unique flood events saved")
    print(f"Output: {OUTPUT_CSV}")