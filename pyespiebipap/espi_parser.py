from datetime import date
import logging
from typing import Any, TypedDict

import pandas as pd

from pyespiebipap.type_defs import BSTag, BSSoup
from pyespiebipap.node import ESPINode

__all__ = ["parse_espi_node_soup"]

logger = logging.getLogger(__name__)


CurrentReport = TypedDict("CurrentReport", {
    "Raport bieżący nr": str,
    "Data sporządzenia": date,
    "Skrócona nazwa emitenta": str,
    "Temat": str,
    "Podstawa prawna": str,
    "Treść raportu": str
})


def _extract_table_of_contents(soup: BSSoup) -> pd.DataFrame:

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


def _extract_entry_from_soup(soup: BSSoup, name: str):
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        for i, cell in enumerate(cells):
            if cell.get_text(strip=True) == name:
                result = " ".join(c.get_text(strip=True) for c in cells)
    return result


def _extract_current_report(soup: BSSoup) -> Any:

    report_number = (
        _extract_entry_from_soup(soup=soup, name="Raport bieżący nr"))
    report_date = (
        _extract_entry_from_soup(soup=soup, name="Data sporządzenia"))


    # out: CurrentReport = {
    #     "Raport bieżący nr": str,
    #     "Data sporządzenia": date,
    #     "Skrócona nazwa emitenta": str,
    #     "Temat": str,
    #     "Podstawa prawna": str,
    #     "Treść raportu": str
    # }

    return {}


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
    from pyespiebipap.common import make_node_soup
    soup = make_node_soup(node_id=714972)
    node = parse_espi_node_soup(soup=soup)
