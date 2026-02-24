from .common import scrape_date_entries, make_node_soup, extract_node_source
from .espi_parser import parse_espi_node_soup

__all__ = [
    "extract_node_source",
    "make_node_soup",
    "parse_espi_node_soup",
    "scrape_date_entries",
]

import logging


def configure_logging():

    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(level=logging.INFO)


configure_logging()
