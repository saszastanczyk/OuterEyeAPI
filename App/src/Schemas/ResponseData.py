from typing import List, Optional

from pydantic import BaseModel

from src.Schemas.UserData import ActionData


class HeaderData(BaseModel):
    h: str
    d: str

class BlockToPlaceData(ActionData):
    t: str
    p: List[int]

class AIResponse(BaseModel):
    b: List[BlockToPlaceData]
    t: Optional[List[int]] = None
    h: List[HeaderData]