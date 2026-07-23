from typing import List

from pydantic import BaseModel

from App.src.Schemas.UserData import PositionScanData, InventoryScanData, ActionData

class PrayResponseRequest(BaseModel):
    u: str
    t: str
    k: int


