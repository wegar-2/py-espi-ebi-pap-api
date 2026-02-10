from datetime import datetime
from typing import Any

import pandas as pd
from pydantic import BaseModel

__all__ = ["Entry"]


class Entry(BaseModel):
    source: str
    dt: datetime
    news_id: str
    title: str
    url: str

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame(data={
            "source": [self.source],
            "dt": [self.dt],
            "news_id": [self.news_id],
            "title": [self.title],
            "url": [self.url]
        })
