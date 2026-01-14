import logging
import requests
from .config import BASE_URL

logger = logging.getLogger(__name__)


def fetch_window(session, start, end, retries=3, timeout=30):
    params = {
        "eventlist": "FL",
        "fromdate": start.isoformat(),
        "todate": end.isoformat(),
        "alertlevel": "green;orange;red",
    }

    for attempt in range(1, retries + 1):
        try:
            r = session.get(BASE_URL, params=params, timeout=timeout)
        except requests.RequestException as exc:
            logger.warning(
                "Request failed",
                extra={
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "attempt": attempt,
                    "error": str(exc),
                },
            )
            continue

        if r.status_code != 200:
            logger.warning(
                "HTTP error while fetching GDACS window",
                extra={
                    "status_code": r.status_code,
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "attempt": attempt,
                },
            )

            continue

        try:
            payload = r.json()
            return payload.get("features", [])
        except ValueError:
            logger.exception(
                "Failed to decode JSON response",
                extra={
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "attempt": attempt,
                },
            )

    logger.error(
        "Skipping GDACS window after repeated failures",
        extra={
            "start": start.isoformat(),
            "end": end.isoformat(),
            "retries": retries,
        },
    )
    return []
