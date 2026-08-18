from typing import Sequence, List, Tuple

import sqlalchemy as sa
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.src.models import User, InventoryScan, PositionScan, Action, KillAction, MealAction, BreedAction
from app.src.schemas.user_data import InventoryScanItemData, InventoryScanData, PositionScanData, MealData, BreedData, \
    KillData, CraftData, DeathData, PrayData, ActionData


class UserDataService:

    @staticmethod
    async def get_origins(user:User,db:AsyncSession,position_in_a_list:int = 10) -> Tuple[List[int],int]:
        """
        Gets as time origin happen_date of one of positions_scans in database as tuple

        """

        query = sa.select(PositionScan).where(PositionScan.user == user).order_by(PositionScan.scan_time).limit(position_in_a_list).options(selectinload(PositionScan.position))
        result = await db.execute(query)

        scan_models: Sequence[PositionScan] = result.scalars().all()
        if  len(scan_models) == 0:
            scan_model = scan_models[-1]

            position = scan_model.position
            time = int(scan_model.scan_time.timestamp())

            return [position.pos_x, position.pos_y, position.pos_z], time
        else:
            return [0,0,0], 0

    @staticmethod
    async def get_inventory_scans(user:User,time_origin:int, limit:int,db:AsyncSession) -> List[InventoryScanData]:
        """
        Gets recent inventory scans as list

        """
        inventory_scans_query = sa.select(InventoryScan).order_by(desc(InventoryScan.time)).options(selectinload(InventoryScan.inventory_scan_items)).where(InventoryScan.user == user) .order_by(InventoryScan.time.desc()).limit(limit)
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
            inventory_scans.append(InventoryScanData(s_t=int(scan.time.timestamp() - time_origin), i_l=inventory_items))
        return inventory_scans

    @staticmethod
    async def get_position_scans(user:User,time_origin:int,limit:int,db:AsyncSession) -> List[PositionScanData]:
        """
        Gets recent position scans as list

        """
        position_scans_query = sa.select(PositionScan).order_by(desc(PositionScan.scan_time)).options(selectinload(PositionScan.position)).where(PositionScan.user == user).order_by(PositionScan.scan_time.desc()).limit(limit)
        positions_scan_result = await db.execute(position_scans_query)
        position_scans_models: Sequence[PositionScan] = positions_scan_result.scalars().all()

        position_scans = []

        for position in position_scans_models:
            position_scans.append(PositionScanData(s_t=int(position.scan_time.timestamp() - time_origin),
                                                   p=[position.position.pos_x, position.position.pos_y,
                                                      position.position.pos_z] ))
        return position_scans

    @staticmethod
    async def get_actions(user:User,time_origin:int,limit:int,db:AsyncSession) -> List[ActionData]:
        """
        Gets list of recent actions(breed,kill,craft,death,pray)

        """
        actions_query = sa.select(Action).order_by(desc(Action.happen_time)).options(
                joinedload(Action.meal_action),
                joinedload(Action.kill_action),
                joinedload(Action.breed_action),
                joinedload(Action.craft_action),
                joinedload(Action.death_action),
                joinedload(Action.pray_action),
                joinedload(Action.position),  # Загружаем сразу и позицию
            ).where(Action.user == user).limit(limit)
        actions_result = await db.execute(actions_query)
        actions_models: Sequence[Action] = actions_result.scalars().all()

        actions = []
        for action in actions_models:
            position = [ action.position.pos_x,action.position.pos_y,action.position.pos_z]
            happen_time = int(action.happen_time.timestamp()) - time_origin
            if action.meal_action is not None:
                actions.append(MealData(
                    p=position,
                    n=action.meal_action.meal_name,
                    h_d=happen_time
                ))
            elif action.kill_action is not None:
                actions.append(KillData(
                    p=position,
                    k_type=action.kill_action.killed_type,
                    k_id=action.kill_action.killed_subject_id,
                    k_n=action.kill_action.killed_name,
                    k_t=action.kill_action.kill_tool,
                    h_d=happen_time
                ))
            elif action.breed_action is not None:
                actions.append(BreedData(
                    p=position,
                    f_id=action.breed_action.father_subject_id,
                    m_id=action.breed_action.mother_subject_id,
                    c_id=action.breed_action.child_subject_id,
                    c_t=action.breed_action.child_type,
                    h_d=happen_time
                ))
            elif action.craft_action is not None:
                data = CraftData(
                    p=position,
                    n=action.craft_action.craft_subject,
                    am=action.craft_action.amount,
                    h_d=happen_time,
                )
                actions.append(data)
            elif action.death_action is not None:
                data = DeathData(
                    p=position,
                    c=action.death_action.death_cause,
                    h_d=happen_time
                )
                actions.append(data)
            elif action.pray_action is not None:
                data = PrayData(
                    p=position,
                    t=action.pray_action.pray_text,
                    r=action.pray_action.pray_respond,
                    h_d=happen_time
                )
                actions.append(data)
        return actions