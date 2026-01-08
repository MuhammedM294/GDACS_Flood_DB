import csv
from datetime import date
from unittest.mock import patch, MagicMock

import pytest

from gdacs_flood_db.pipeline import download_all_floods
from gdacs_flood_db.utils.download_db_utils import normalize_flood_event
from gdacs_flood_db.schema import FLOOD_FIELDS

TEST_EVENT = {
    "properties": {
        "eventid": "TEST123",
        "eventtype": "Flood",
        "glide": "GL123",
        "alertlevel": "green",
        "alertscore": 1,
        "episodealertlevel": "green",
        "episodealertscore": 1,
        "country": "Testland",
        "fromdate": "2026-01-01T00:00:00Z",
        "todate": "2026-01-02T00:00:00Z",
        "datemodified": "2026-01-01T12:00:00Z",
        "source": "GDACS",
        "affectedcountries": ["Testland"],
        "geometry_url": "https://example.com/geometry",
        "report_url": "https://example.com/report",
        "details_url": "https://example.com/details",
        "bbox": [0, 0, 1, 1],
        "location_type": "Point",
        "location_coordinates": [0.5, 0.5],
    }
}

NORMALIZED_EVENT = normalize_flood_event(TEST_EVENT)

@pytest.fixture
def tmp_csv_path(tmp_path):
    return tmp_path / "gdacs_flood_db.csv"

@patch("gdacs_flood_db.pipeline.fetch_window")
@patch("gdacs_flood_db.pipeline.requests.Session")
@patch("gdacs_flood_db.pipeline.month_windows")
def test_download_all_floods(mock_month_windows, mock_session_class, mock_fetch_window, tmp_csv_path):
    start = date(2026, 1, 1)
    end = date(2026, 1, 1)

    # Mock month_windows to return exactly one window
    mock_month_windows.return_value = [(start, end)]

    # Mock requests.Session
    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session

    # Mock fetch_window to return our TEST event
    mock_fetch_window.return_value = [TEST_EVENT]

    # Patch OUTPUT_CSV to temporary file
    with patch("gdacs_flood_db.pipeline.OUTPUT_CSV", tmp_csv_path):
        download_all_floods(start_date=start, end_date=end)

    # Read CSV
    with open(tmp_csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Header matches
    assert reader.fieldnames == FLOOD_FIELDS

    # Only one row
    assert len(rows) == 1

    # All fields match (handle None -> '')
    for field in FLOOD_FIELDS:
        expected = '' if NORMALIZED_EVENT[field] is None else str(NORMALIZED_EVENT[field])
        assert rows[0][field] == expected

    # fetch_window called correctly
    mock_fetch_window.assert_called_once_with(mock_session, start, end)


if __name__ == "__main__":
    pytest.main([__file__])