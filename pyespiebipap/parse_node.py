import logging
from typing import Any, TypeAlias

import bs4
import pandas as pd
import requests

from pyespiebipap.common import BSTag

Response: TypeAlias = requests.models.Response


__all__ = ["parse_node"]

logger = logging.getLogger(__name__)


def _make_node_id(node_num: int) -> str:
    return f"https://espiebi.pap.pl/node/{node_num}"


def _extract_table_of_contents(
        response: Response,
        node_num: int
) -> pd.DataFrame:
    logger.info(f"Extracting Table of Contents from node {node_num}")
    soup = bs4.BeautifulSoup(response.text, "lxml")
    toc: BSTag = soup.find("div", class_="table-of-contents")
    toc_points: list[BSTag] = toc.find_all("a")

    rows: list[pd.DataFrame] = []

    for point in toc_points:
        rows.append(
            pd.DataFrame(data={
                "name": [point.text],
                "section": [point.get("href").lstrip("#")]
            })
        )
    return pd.concat(rows, axis=0).reset_index(drop=True)


def _parse_table_of_contents(response) -> Any:

    return response


def _extract_entity_info():
    pass


def _extract_signatures():
    pass


def _extract_attachments():
    pass


def parse_node(node_num: int) -> Any:

    node_url: str = _make_node_id(node_num=node_num)

    logging.info(f"Getting node content from {node_url=}")
    response: Response = requests.get(node_url)
    response.raise_for_status()

    toc: pd.DataFrame = _extract_table_of_contents(
        response=response, node_num=node_num)


if __name__ == "__main__":
    parse_node(node_num=714972)
