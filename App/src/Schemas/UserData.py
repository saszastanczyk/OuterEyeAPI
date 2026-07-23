import uuid

from typing import Optional, List, Literal, Annotated, Union

from pydantic import BaseModel, Field

class ActionData(BaseModel):
    p: List[int]
    h_t: int

class MealData(ActionData):
    a: Literal["meal"] = "meal"
    n: str

class KillData(ActionData):
    a: Literal["kill"] = "kill"
    k_type: str
    k_id: Optional[uuid.UUID] = None
    k_n: Optional[str] = None
    k_t: str

class BreedData(ActionData):
    a: Literal["breed"] = "breed"
    f_id: uuid.UUID
    m_id: uuid.UUID
    c_id: uuid.UUID
    c_t: str

class CraftData(ActionData):
    a: Literal["craft"] = "craft"
    n:str
    am: int

class DeathData(ActionData):
    a: Literal["death"] = "death"
    c: str

class PrayData(ActionData):
    a: Literal["pray"] = "pray"
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


ActionList = Annotated[Union[PrayData,DeathData,CraftData,MealData,BreedData,KillData],Field(discriminator="a")]

class UserData(BaseModel):
    u: str
    i_s: List[InventoryScanData]
    p_s: List[PositionScanData]
    a_l: List[ActionList]
