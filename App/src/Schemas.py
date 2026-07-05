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
    position: PositionScanSchema
    items: List[InventoryScanItemSchema]