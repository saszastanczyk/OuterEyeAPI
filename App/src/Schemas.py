import uuid
from typing import List

from pydantic import BaseModel



class PositionScanSchema(BaseModel):
    pos_x: int
    pos_y: int
    pos_z: int

class InventoryScanItemSchema(BaseModel):
    item_name: str
    item_amount: int

class InventoryScanSchema(BaseModel):
    items: List[InventoryScanItemSchema]

class MealActionSchema(BaseModel):
    position: PositionScanSchema
    meal_name: str

class CraftActionSchema(BaseModel):
    position: PositionScanSchema
    craft_subject:str
    craft_amount: int

class KillActionSchema(BaseModel):
    position: PositionScanSchema
    kill_type: str
    kill_subject: uuid.UUID
    kill_tool: str

class BreedActionSchema(BaseModel):
    position: PositionScanSchema
    father_subject_id: uuid.UUID
    mother_subject_id: uuid.UUID
    child_subject_id: uuid.UUID

class DeathActionSchema(BaseModel):
    position: PositionScanSchema
    death_cause:str