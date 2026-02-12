import logging
from typing import Any, Optional

import bs4
import pandas as pd
import requests

from pyespiebipap.type_defs import BSTag, BSSoup, NodeSource, Response
from pyespiebipap.node import ESPINode

__all__ = ["parse_espi_node_soup"]

logger = logging.getLogger(__name__)


def _extract_table_of_contents(soup: BSSoup) -> pd.DataFrame:

    logging.info(f"Getting node content from {node_url=}")

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


def _extract_current_report(
        soup: BSSoup,
        toc: pd.DataFrame
) -> Any:

    container = soup.find("div", class_="arkusz")
    table = container.find("table")

    rows = table.find_all("tr")

    data = {}
    last_label = None

    for row in rows:
        cells = row.find_all("td")
        texts = [
            cell.get_text(
                separator=" ", # noqa
                strip=True
            )
            for cell in cells
            if cell.get_text(strip=True)
        ]

        if not texts:
            continue

        if len(texts) == 1:
            if last_label:
                data[last_label] += "\n" + texts[0]
        elif len(texts) >= 2:
            key = texts[0]
            value = " ".join(texts[1:])

            data[key] = value
            last_label = key

    return response


def _extract_entity_info():
    pass


def _extract_signatures():
    pass


def _extract_attachments():
    pass


def parse_espi_node_soup(soup: BSSoup) -> ESPINode:

    toc: pd.DataFrame = _extract_table_of_contents(soup=soup)

    current_report = _extract_current_report(soup=soup)

    return ESPINode(
        toc=toc,
        current_report=current_report
    )


if __name__ == "__main__":
    # parse_node_soup()
    pass
