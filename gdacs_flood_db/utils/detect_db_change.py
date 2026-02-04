from pathlib import Path
import pandas as pd

TRACKED_FIELDS = ["fromdate", "todate", "geometry_url"]


def detect_updated_events(
    df_new: pd.DataFrame,
    df_old: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect existing GDACS events whose tracked fields changed.
    Returns rows from df_new that should overwrite old records.
    """

    # Index by GDACS_ID for safe alignment
    old = df_old.set_index("GDACS_ID")
    new = df_new.set_index("GDACS_ID")

    updated_rows = []

    for gdacs_id in new.index.intersection(old.index):
        changes = {}

        for field in TRACKED_FIELDS:
            old_val = old.at[gdacs_id, field]
            new_val = new.at[gdacs_id, field]

            # Handle NaNs safely
            if pd.isna(old_val) and pd.isna(new_val):
                continue

            if old_val != new_val:
                changes[field] = {
                    "old": old_val,
                    "new": new_val,
                }

        if changes:
            row = new.loc[gdacs_id].copy()
            row["changed_fields"] = list(changes.keys())
            row["change_details"] = changes
            updated_rows.append(row)

    if not updated_rows:
        return pd.DataFrame()

    return pd.DataFrame(updated_rows).reset_index()


if __name__ == "__main__":
    # Example usage
    DATA_DIR = Path(__file__).parent.parent.parent / "data"
    BASE_DB = DATA_DIR / "gdacs_flood_db.csv"
    NEW_DB = DATA_DIR / "gdacs_flood_db_20260204.csv"  # Example new DB

    df_new = pd.read_csv(NEW_DB)
    df_old = pd.read_csv(BASE_DB)

    changed_events = detect_updated_events(df_new, df_old)
    print(f"Changed existing events: {len(changed_events)}")
    if not changed_events.empty:
        print(changed_events)
