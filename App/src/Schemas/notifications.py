import uuid
from typing import List, Optional

from pydantic import BaseModel

class PositionNotification(BaseModel):
    pos_x:int
    pos_y:int
    pos_z:int

class InventoryItemNotification(BaseModel):
    name:str
    amount:int

class InventoryScanNotification(BaseModel):
    items:List[InventoryItemNotification]

class ActionNotification(BaseModel):
    position: PositionNotification

class MealNotification(ActionNotification):
    meal_name: str

class CraftNotification(ActionNotification):
    craft_subject:str
    craft_amount: int

class KillNotification(ActionNotification):
    kill_type: str
    kill_subject: Optional[uuid.UUID] = None
    kill_name:  Optional[str] = None
    kill_tool: str

class BreedNotification(ActionNotification):
    father_subject_id: uuid.UUID
    mother_subject_id: uuid.UUID
    child_subject_id: uuid.UUID
    child_type: str

class DeathNotification(ActionNotification):
    death_cause:str

class PrayNotification(ActionNotification):
    pray_text: str
