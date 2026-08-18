import logging

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter
from fastapi import Depends, HTTPException

from app.src.database import get_db
from app.src.models import PositionScan, Position, InventoryScanItem, InventoryScan
from app.src.auth import CurrentUser
from app.src.schemas.notifications import PositionNotification,InventoryScanNotification

router = APIRouter(prefix="/scan")

@router.post("/position")
async def add_position_scan(scan:PositionNotification ,user:CurrentUser,db:AsyncSession = Depends(get_db)):
    try:
        position = Position(
            pos_x=scan.pos_x,
            pos_y=scan.pos_y,
            pos_z=scan.pos_z,
        )
        db.add(position)

        position_scan = PositionScan(
            user=user,
            position=position,
        )

        db.add(position_scan)
        await db.commit()
        return {"status":"created"}
    except Exception as e:
        await db.rollback()
        logging.error( f"Error on adding position scan: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/inventory")
async def add_inventory_scan(scan:InventoryScanNotification,user:CurrentUser,db:AsyncSession = Depends(get_db)):
    try:
        inventory_items = [InventoryScanItem(item_name=item.name,amount=item.amount) for item in scan.items]

        inventory_scan = InventoryScan(
            user=user,
            inventory_scan_items=inventory_items
        )

        db.add(inventory_scan)
        await db.commit()

        return {"status":"created"}

    except Exception as e:
        await db.rollback()
        logging.error( f"Error on adding inventory scan: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
