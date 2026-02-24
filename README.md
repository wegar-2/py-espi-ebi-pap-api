# pyespiebipapapi

![Flake8 Lint Check](https://github.com/wegar-2/py-espi-ebi-pap-api/actions/workflows/flake8-lint.yml/badge.svg)

## ESPI, EBI and PAP
This package provides interface for retrieval of
data published at the 
[ESPI and EBI news website of PAP](https://espiebi.pap.pl/).
 
PAP is *Polish Press Agency* (Polish: *Polska Agencja Prasowa*). 

The two eponymous news systems from which the news are sourced are:
* [ESPI](https://www.knf.gov.pl/dla_rynku/espi) - Polish: 
*Elektroniczny System Przekazywania Informacji*, English: 
*Electronic System for Information Transfer*
* [EBI](https://www.sii.org.pl/5986/ochrona-praw/eksperci-sii-radza/co-to-jest-espi-i-ebi.html) - 
Polish: *Elektroniczna Baza Informacji*, English: *Electronic Information Base*

## Installation

This package is in development and is not yet published at PyPI.
You can install it by running: 
```commandline
pip install git+https://github.com/wegar-2/py-espi-ebi-pap.git@master
```


## Examples

### Retrieve All Entries Published on a Given Date

```python
from datetime import date
from pyespiebipapapi import scrape_date_entries

entries = scrape_date_entries(date(2026, 2, 6))
```

### Get bs4 Soup from Node by ID

```python
from pyespiebipapapi import make_node_soup

node = make_node_soup(node_id=715_032)
```

### Check if Node is an ESPI or EBI Node

```python
from pyespiebipapapi import extract_node_source, make_node_soup

source = extract_node_source(
    node_soup=make_node_soup(node_id=715_032)
)
print(f"{source=}")
```

### Parse Single ESPI Node

```python
from pyespiebipapapi import parse_espi_node_soup, make_node_soup

node_data = parse_espi_node_soup(
    soup=make_node_soup(node_id=715_032)
)
```
