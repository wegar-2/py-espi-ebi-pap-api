from typing import Literal, TypeAlias

import bs4
import requests

__all__ = ["BSTag", "BSSoup", "Response", "NodeSource"]


BSTag: TypeAlias = bs4.element.Tag
BSSoup: TypeAlias = bs4.BeautifulSoup
Response: TypeAlias = requests.models.Response

NodeSource: TypeAlias = Literal["ESPI", "EBI"]
