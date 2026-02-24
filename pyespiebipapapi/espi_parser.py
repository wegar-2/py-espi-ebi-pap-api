from datetime import date, datetime
import logging
from typing import Any, TypedDict

import pandas as pd

from pyespiebipapapi.type_defs import BSTag, BSSoup
from pyespiebipapapi.node import ESPINode

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


def _extract_top_entity_info(soup: BSSoup) -> pd.DataFrame:
    table_info = soup.find("table", class_="nDokument")
    rows = table_info.find_all("tr")
    parsed_rows: list[dict] = []
    for row in rows:
        # row = rows[0]
        name, value = row.find_all("td")
        parsed_rows.append({
            "name": name.get_text(strip=True),
            "value": value.get_text(strip=True)
        })
    return pd.DataFrame(data=parsed_rows)


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
    raise Exception()


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
    raise Exception()


def _extract_current_report(soup: BSSoup) -> Any:
    return {
        "Raport bieżący nr": _extract_single_line_entry_from_soup(
            soup=soup, name="Raport bieżący nr"),
        "Data sporządzenia": datetime.strptime(
            _extract_single_line_entry_from_soup(
                soup=soup, name="Data sporządzenia"
            ), "%Y-%m-%d"
        ),
        "Skrócona nazwa emitenta": _extract_two_lines_entry_from_soup(
            soup=soup, name="Skrócona nazwa emitenta"),
        "Temat": _extract_two_lines_entry_from_soup(
            soup=soup, name="Temat"),
        "Podstawa prawna": _extract_two_lines_entry_from_soup(
            soup=soup, name="Podstawa prawna"),
        "Treść raportu": _extract_two_lines_entry_from_soup(
            soup=soup, name="Treść raportu:")
    }


def _extract_entity_info(soup: BSSoup):

    marker = soup.find(string=lambda s: s and "(pełna nazwa emitenta)" in s)
    if not marker:
        return None

    table = marker.find_parent("table")
    if not table:
        return None

    rows = [
        [td.get_text(strip=True) for td in tr.find_all("td")]
        for tr in table.find_all("tr")
    ]

    def first_value(row):
        values = [x for x in row if x and not x.startswith("(")]
        return values[0] if values else None
    data = {}

    for i, row in enumerate(rows):
        if any("(pełna nazwa emitenta)" in cell for cell in row):
            data["pelna_nazwa"] = first_value(rows[i - 1])

        if any("(skrócona nazwa emitenta)" in cell for cell in row):
            prev_row = rows[i - 1]
            values = [x for x in prev_row if x and not x.startswith("(")]
            if len(values) >= 1:
                data["skrocona_nazwa"] = values[0]
            if len(values) >= 2:
                data["sektor"] = values[1]

        if any("(kod pocztowy)" in cell for cell in row):
            prev_row = rows[i - 1]
            values = [x for x in prev_row if x and not x.startswith("(")]
            if len(values) >= 1:
                data["kod_pocztowy"] = values[0]
            if len(values) >= 2:
                data["miasto"] = values[1]

        if any("(ulica)" in cell for cell in row):
            prev_row = rows[i - 1]
            values = [x for x in prev_row if x and not x.startswith("(")]
            if len(values) >= 1:
                data["ulica"] = values[0]
            if len(values) >= 2:
                data["numer"] = values[1]

        if any("(e-mail)" in cell for cell in row):
            prev_row = rows[i - 1]
            values = [x for x in prev_row if x and not x.startswith("(")]
            if len(values) >= 1:
                data["email"] = values[0]
            if len(values) >= 2:
                data["www"] = values[1]

        if any("(NIP)" in cell for cell in row):
            prev_row = rows[i - 1]
            values = [x for x in prev_row if x and not x.startswith("(")]
            if len(values) >= 1:
                data["nip"] = values[0]
            if len(values) >= 2:
                data["regon"] = values[1]

    return data


def _extract_signatures(soup: BSSoup) -> pd.DataFrame:
    section = None
    for x in soup.find_all("div", class_="arkusz"):
        if x.find(string="PODPISY OSÓB REPREZENTUJĄCYCH SPÓŁKĘ"):
            section = x
    if section is None:
        raise ValueError()

    table = section.find("table")
    rows = table.find_all("tr")

    headers = [
        cell.get_text(strip=True)
        for cell in rows[1].find_all("td")
        if cell.get_text(strip=True)
    ]

    results = []
    for row in rows[2:]:
        cells = [
            cell.get_text(strip=True)
            for cell in row.find_all("td")
            if cell.get_text(strip=True)
        ]
        if cells:
            results.append(dict(zip(headers, cells)))

    return pd.DataFrame(data=results)


def parse_espi_node_soup(soup: BSSoup) -> ESPINode:
    return ESPINode(
        toc=_extract_table_of_contents(soup=soup),
        top_entity_info=_extract_top_entity_info(soup=soup),
        current_report=_extract_current_report(soup=soup),
        signatures=_extract_signatures(soup=soup),
        entity_info=_extract_entity_info(soup=soup),
    )
