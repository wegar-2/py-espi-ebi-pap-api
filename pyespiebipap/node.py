from typing import Any, Optional

import pandas as pd
from pydantic import BaseModel, ConfigDict

__all__ = ["ESPINode", "EBINode"]


class ESPINode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    toc: pd.DataFrame
    current_report: Optional[pd.DataFrame] = None
    current_report_en: Optional[pd.DataFrame] = None
    entity_info: Optional[pd.DataFrame] = None
    signatures: Optional[pd.DataFrame] = None
    attachments: Optional[list[Any]] = None



class EBINode(BaseModel):
    pass
