import logging
from typing import Any

import requests

__all__ = ["parse_node"]

logger = logging.getLogger(__name__)


def _extract_table_of_contents(response) -> Any:
    pass


def _parse_table_of_contents(response) -> Any:

    return response


def _extract_entity_info():
    pass


def _extract_signatures():
    pass


def _extract_attachments():
    pass


def parse_node(url: str) -> Any:

    logging.info(f"Getting node content from {url=}")
    response = requests.get(url)
    response.raise_for_status()

    logger.info("Determining node structure based on table of contents")
    toc = _extract_table_of_contents(response)

    logger.info("")
