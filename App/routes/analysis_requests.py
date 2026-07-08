import logging
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette.responses import JSONResponse

from App.src.Database import get_db
from App.src.Auth import CurrentUser
from src.OpenAI import get_analysis_response
from src.Schemas.Requests import DataAnalysisRequest

from src.Services import UserDataService

router = APIRouter(prefix="/analysis")

@router.get("/scenario")
async def get_response_scenario(user: CurrentUser,db: AsyncSession = Depends(get_db)):
    try:
        request = DataAnalysisRequest(
            u=user.username,
            i_s= await UserDataService.get_inventory_scans(user, 20, db),
            p_s= await UserDataService.get_position_scans(user, 20, db),
            a_l= await UserDataService.get_actions(user, 20, db)
        )

        response = await get_analysis_response(request)

        print(response)

        return JSONResponse(status_code=200, content={"analysis_respond":response})


    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail="Internal Server Error")