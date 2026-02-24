from typing import Any, Optional

import pandas as pd
from pydantic import BaseModel, ConfigDict

__all__ = ["ESPINode", "EBINode"]


class ESPINode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    toc: pd.DataFrame
    top_entity_info: pd.DataFrame
    current_report: dict
    current_report_en: Optional[pd.DataFrame] = None
    entity_info: pd.DataFrame | dict
    signatures: pd.DataFrame
    attachments: Optional[list[Any]] = None


class EBINode(BaseModel):
    pass
