from typing import List, Optional, Dict

from pydantic import BaseModel

from src.Schemas.user_data import ActionData

class HeaderData(BaseModel):
    h: str #header
    d: str #description

class EnhancementData(BaseModel):
    t: str #enhancement type
    l: int #enhancement level

class ItemData(BaseModel):
    n: Optional[str] #name og item
    t: str #item type
    d: Optional[str] #item description
    e: Optional[List[EnhancementData]] #list of enhancements
    a: int #amount

class EntityData(BaseModel):
    t:str #entity type
    r: Optional['EntityData'] #rider data
    e: Optional[List[ItemData]] #equipment
    p: List[int] #entity summon position
    a: int #amount of entities to summon

class AIResponse(BaseModel):
    b: Optional[Dict[str,List[int]]] #list of blocks to place (dict of block type as key and list of positions where blocks og this type should be pasted)
    e: Optional[List[EntityData]] #list of entities to summon
    i: Optional[List[ItemData]] #list of items to give to a player
    t: Optional[List[int]] #position a player should be teleported to
    r: str #little review of player's action and description of god's will
    h: HeaderData #data of message which plugin shows on performing god's will

if __name__ == '__main__':
        print(AIResponse.model_json_schema())