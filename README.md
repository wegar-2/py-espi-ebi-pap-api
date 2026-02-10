# py-espi-ebi-pap

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

As the package is in development, contents of this section are rather limited
for now. 

### Retrieve All Entries Published on a Given Date
```python
from datetime import date
from pyespiebipap import scrape_date_entries

entries = scrape_date_entries(date(2026, 2, 6))
```
