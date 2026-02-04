from gdacs_flood_db.pipeline import download_all_floods
from gdacs_flood_db.logger import setup_logging
import logging

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    setup_logging()
    download_all_floods()
    logger.info("Flood events downloaded")
