import logging

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette.responses import JSONResponse

from app.src.database import get_db
from app.src.auth import CurrentUser
from app.src.open_ai import get_analysis_response
from app.src.schemas.user_data import UserData

from app.src.services import UserDataService

router = APIRouter(prefix="/analysis")

@router.get("/scenario")
async def get_response_scenario(user: CurrentUser,db: AsyncSession = Depends(get_db)):
    try:
        origin_pos, origin_time = await UserDataService.get_origins(user, db,20)

        request = UserData(
            u=user.username,
            time_origin=origin_time,
            i_s= await UserDataService.get_inventory_scans(user,origin_time, 2,db),
            p_s= await UserDataService.get_position_scans(user,origin_time, 50, db),
            a_l= await UserDataService.get_actions(user,origin_time,100, db)
        )

        response = await get_analysis_response(request)

        return JSONResponse(status_code=200, content={"analysis_respond":response.model_dump_json()})


    except Exception as ex:
        logging.error(f"Error on handing scenarios request:{str(ex)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")