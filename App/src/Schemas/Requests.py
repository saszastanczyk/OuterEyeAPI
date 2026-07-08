from typing import List

from pydantic import BaseModel

from src.Schemas.UserData import PositionScanData, InventoryScanData, ActionData

class PrayResponseRequest(BaseModel):
    u: str
    t: str
    k: int

class DataAnalysisRequest(BaseModel):
    u: str
    i_s: List[InventoryScanData]
    p_s: List[PositionScanData]
    a_l: List[ActionData]
