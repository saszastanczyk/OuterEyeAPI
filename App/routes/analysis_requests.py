import logging
import traceback

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette.responses import JSONResponse

from App.src.Database import get_db
from App.src.Auth import CurrentUser
from App.src.OpenAI import get_analysis_response
from App.src.Schemas.UserData import UserData

from App.src.Services import UserDataService

router = APIRouter(prefix="/analysis")

@router.get("/scenario")
async def get_response_scenario(user: CurrentUser,db: AsyncSession = Depends(get_db)):
    try:
        request = UserData(
            u=user.username,
            i_s= await UserDataService.get_inventory_scans(user, 2, db),
            p_s= await UserDataService.get_position_scans(user, 20, db),
            a_l= await UserDataService.get_actions(user, 100, db)
        )

        print(request.model_dump_json())
        response = await get_analysis_response(request)

        print(response)

        return JSONResponse(status_code=200, content={"analysis_respond":response})


    except Exception as ex:
        logging.error(ex)
        logging.error(str(ex.message))
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")