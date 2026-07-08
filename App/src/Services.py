from typing import Sequence, List

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.Models import User, InventoryScan, PositionScan, Action
from src.Schemas.UserData import InventoryScanItemData, InventoryScanData, PositionScanData, MealData, BreedData, \
    KillData, CraftData, DeathData, PrayData, ActionData


class UserDataService:

    @staticmethod
    async def get_inventory_scans(user:User,limit:int,db:AsyncSession) -> List[InventoryScanData]:
        inventory_scans_query = sa.select(InventoryScan).options(selectinload(InventoryScan.inventory_scan_items)).where(InventoryScan.user == user) .order_by(InventoryScan.time.desc()).limit(limit)
        inventory_scans_result = await db.execute(inventory_scans_query)
        inventory_scans_models: Sequence[InventoryScan] = inventory_scans_result.scalars().all()

        inventory_scans = []

        for scan in inventory_scans_models:
            inventory_items = []
            for item in scan.inventory_scan_items:
                inventory_items.append(InventoryScanItemData(
                    n=item.item_name,
                    a=item.amount
                ))
            inventory_scans.append(InventoryScanData(s_t=int(scan.time.timestamp()), i_l=inventory_items))
        return inventory_scans

    @staticmethod
    async def get_position_scans(user:User,limit:int,db:AsyncSession) -> List[PositionScanData]:
        position_scans_query = sa.select(PositionScan).options(selectinload(PositionScan.position)).where(PositionScan.user == user).order_by(PositionScan.scan_time.desc()).limit(limit)
        positions_scan_result = await db.execute(position_scans_query)
        position_scans_models: Sequence[PositionScan] = positions_scan_result.scalars().all()

        position_scans = []

        for position in position_scans_models:
            position_scans.append(PositionScanData(s_t=int(position.scan_time.timestamp()),
                                                   p=[position.position.pos_x, position.position.pos_y,
                                                      position.position.pos_z]))
        return position_scans

    @staticmethod
    async def get_actions(user:User,limit:int,db:AsyncSession) -> List[ActionData]:
        actions_query = sa.select(Action).options(
                selectinload(Action.meal_action),
                selectinload(Action.kill_action),
                selectinload(Action.breed_action),
                selectinload(Action.craft_action),
                selectinload(Action.death_action),
                selectinload(Action.pray_action),
                selectinload(Action.position),  # Загружаем сразу и позицию
            ).where(Action.user == user).limit(limit)
        actions_result = await db.execute(actions_query)
        actions_models: Sequence[Action] = actions_result.scalars().all()

        actions = []
        for action in actions_models:
            position = [action.position.pos_x, action.position.pos_y,action.position.pos_z]
            happen_time = int(action.happen_time.timestamp())
            if action.meal_action is not None:
                actions.append(MealData(
                    p=position,
                    n=action.meal_action.meal_name,
                    h_t=happen_time
                ))
            elif action.kill_action is not None:
                actions.append(KillData(
                    p=position,
                    k_type=action.kill_action.killed_type,
                    k_id=action.kill_action.killed_subject_id,
                    k_n=action.kill_action.killed_name,
                    k_t=action.kill_action.kill_tool,
                    h_t=happen_time
                ))
            elif action.breed_action is not None:
                actions.append(BreedData(
                    p=position,
                    f_id=action.breed_action.father_subject_id,
                    m_id=action.breed_action.mother_subject_id,
                    c_id=action.breed_action.child_subject_id,
                    c_t=action.breed_action.child_type,
                    h_t=happen_time
                ))
            elif action.craft_action is not None:
                actions.append(CraftData(
                    p=position,
                    n=action.craft_action.craft_subject,
                    am=action.craft_action.amount,
                    h_t=happen_time,
                ))
            elif action.death_action is not None:
                actions.append(DeathData(
                    p=position,
                    c=action.death_action.death_cause,
                    h_t=happen_time
                ))
            elif action.pray_action is not None:
                actions.append(PrayData(
                    p=position,
                    t=action.pray_action.pray_text,
                    r=action.pray_action.pray_respond,
                    h_t=happen_time
                ))
        return actions