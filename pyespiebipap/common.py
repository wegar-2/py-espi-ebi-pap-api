from datetime import date, datetime
import logging
from typing import TypeAlias

import bs4
import pandas as pd
import requests

from pyespiebipap.constants import DEFAULT_DATE_FORMAT
from pyespiebipap.entry import Entry

logger = logging.getLogger(__name__)

__all__ = ["scrape_date_entries"]

BSTag: TypeAlias = bs4.element.Tag


def _make_single_date_url(d: date) -> str:
    return (f"https://espiebi.pap.pl/wyszukiwarka?"
            f"created={d.strftime(DEFAULT_DATE_FORMAT)}&"
            f"enddate={d.strftime(DEFAULT_DATE_FORMAT)}+23%3A59")


def _make_single_date_and_page_url(d: date, page: int) -> str:
    ds: str = d.strftime(DEFAULT_DATE_FORMAT)
    return (f"https://espiebi.pap.pl/wyszukiwarka?"
            f"created={ds}&"
            f"enddate={ds}%2023%3A59&"
            f"page={page}")


def _is_news(li: BSTag) -> bool:
    return True if li.get("class", default=None) == ["news"] else False


def _full_url_from_node(node: str) -> str:
    if node[0] == "/":
        node = node[1:]
    return f"https://espiebi.pap.pl/{node}"


def _parse_title(title: str) -> str:
    return title.strip("\n").strip(" ").strip("\n").strip(" ")


def _parse_list_item(li: BSTag, d: date) -> Entry:
    ts_, new_id_ = li.find_all("div", class_="hour")
    return Entry(
        source=str(li.find("div", class_="badge").text).upper(),
        dt=datetime.combine(
            date=d,
            time=datetime.strptime(ts_.text, "%H:%M").time()
        ),
        news_id=new_id_.text,
        title=_parse_title(title=li.find("a").text),
        url=_full_url_from_node(node=li.find("a").get("href"))
    )


def _natural_numbers_generator():
    n = 0
    while True:
        yield n
        n += 1


def _scrape_date_entries_page(d: date, page: int) -> pd.DataFrame:
    url: str = _make_single_date_and_page_url(d=d, page=page)

    logger.info(f"Getting response from {url}")
    response = requests.get(url=url)
    response.raise_for_status()

    logger.info("Making a bs4 soup")
    soup = bs4.BeautifulSoup(response.text, "lxml")

    logger.info("Extracting ESPI/EBI entries from the soup")
    results_section = soup.find_all("li")
    entries: list[Entry | Exception] = []
    results_section_elements_count: int = len(results_section)
    for i, li in enumerate(results_section, start=1):
        logger.info(f"Parsing entry {i}/{results_section_elements_count}")
        if _is_news(li):
            entries.append(_parse_list_item(li=li, d=d))

    data = pd.concat([e.to_row() for e in entries], axis=0)
    data = data.sort_values(by="dt", ascending=True)
    return data.reset_index(drop=True)


def scrape_date_entries(d: date):
    logger.info(f"Scraping ESPI & EBI entries published by PAP "
                f"for date {d.strftime(DEFAULT_DATE_FORMAT)}")
    datas: list[pd.DataFrame] = []

    for page in _natural_numbers_generator():
        logger.info(f"Before scraping page {page} with entries "
                    f"for date {d.strftime(DEFAULT_DATE_FORMAT)}")
        try:
            entries: pd.DataFrame = _scrape_date_entries_page(d=d, page=page)
        except Exception:
            logger.info(f"Failed attempting to scrape page {page}"
                        f"for date {d.strftime(DEFAULT_DATE_FORMAT)}")
            break
        else:
            datas.append(entries)

    data = pd.concat(
        datas, axis=0
    ).sort_values(by="dt", ascending=True).reset_index(drop=True)

    return data
