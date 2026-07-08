import uuid

from typing import Optional,List

from pydantic import BaseModel, Field

class ActionData(BaseModel):
    a: str
    p: List[int]
    h_t: int

class MealData(ActionData):
    a: str = "meal"
    n: str


class KillData(ActionData):
    a: str = "kill"
    k_type: str
    k_id: Optional[uuid.UUID] = None
    k_n: Optional[str] = None
    k_t: str

class BreedData(ActionData):
    a: str = "breed"
    f_id: uuid.UUID
    m_id: uuid.UUID
    c_id: uuid.UUID
    c_t: str

class CraftData(ActionData):
    a: str = "craft"
    n:str
    am: int

class DeathData(ActionData):
    a: str = "death"
    c: str

class PrayData(ActionData):
    a: str = "pray"
    t: str
    r: str

class PositionScanData(BaseModel):
    p: List[int]
    s_t: int

class InventoryScanItemData(BaseModel):
    n:str
    a:int

class InventoryScanData(BaseModel):
    i_l: List[InventoryScanItemData]
    s_t: int

class UserData(BaseModel):
    u: str
    i_s: List[InventoryScanData]
    p_s: List[PositionScanData]
    a_l: List[ActionData]
