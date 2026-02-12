from datetime import date, datetime
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


def _extract_single_line_entry_from_soup(soup: BSSoup, name: str):
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        for i, cell in enumerate(cells):
            if cell.get_text(strip=True) == name:
                result = " ".join(
                    c.get_text(strip=True)
                    for c in cells
                    if c.get_text(strip=True) != name
                )
                return result
    raise Exception


def _extract_two_lines_entry_from_soup(soup: BSSoup, name: str):
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        for cell in cells:
            if cell.get_text(strip=True) == name:
                next_row = row.find_next_sibling("tr")
                if next_row:
                    value_cell = next_row.find("td", colspan="11")
                    if value_cell:
                        return value_cell.get_text(strip=True)
    raise Exception


def _extract_current_report(soup: BSSoup) -> Any:
    number = (
        _extract_single_line_entry_from_soup(
            soup=soup, name="Raport bieżący nr"))
    date_ = (
        _extract_single_line_entry_from_soup(
            soup=soup, name="Data sporządzenia"))
    issuer_short_name = _extract_two_lines_entry_from_soup(
        soup=soup, name="Skrócona nazwa emitenta")
    subject = _extract_two_lines_entry_from_soup(
        soup=soup, name="Temat")
    legal_basis = _extract_two_lines_entry_from_soup(
        soup=soup, name="Podstawa prawna")
    report_text = _extract_two_lines_entry_from_soup(
        soup=soup, name="Treść raportu:")

    return {
        "Raport bieżący nr": number,
        "Data sporządzenia": datetime.strptime(date_, "%Y-%m-%d"),
        "Skrócona nazwa emitenta": issuer_short_name,
        "Temat": subject,
        "Podstawa prawna": legal_basis,
        "Treść raportu": report_text
    }


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
