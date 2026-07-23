import logging
import time

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette.responses import JSONResponse

from App.src.Database import get_db
from App.src.Models import Position, Action, MealAction, KillAction, BreedAction, DeathAction, CraftAction, PrayAction
from App.src.Auth import CurrentUser
from App.src.OpenAI import get_pray_response

from App.src.Schemas.Notifications import MealNotification,CraftNotification,KillNotification,BreedNotification,DeathNotification,PrayNotification
from App.src.Schemas.Requests import PrayResponseRequest

router = APIRouter(prefix="/action")

@router.post("/meal")
async def add_meal( meal: MealNotification,user:CurrentUser,db:AsyncSession = Depends(get_db)):
    try:
        start = time.time()
        position = Position(
            pos_x=meal.position.pos_x,
            pos_y=meal.position.pos_y,
            pos_z=meal.position.pos_z
        )

        meal_action = MealAction(
            meal_name=meal.meal_name,
        )

        action = Action(
            user=user,
            position=position,
            meal_action=meal_action
        )

        db.add(action)
        await db.commit()

        print(f"Delay:{time.time() - start:.2f}")
        return {"status":"created"}

    except Exception as e:
        await db.rollback()
        logging.error(f"Error on handing meal action:{str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/craft")
async def add_craft( craft: CraftNotification,user:CurrentUser,db:AsyncSession = Depends(get_db)):
    try:
        position = Position(
            pos_x=craft.position.pos_x,
            pos_y=craft.position.pos_y,
            pos_z=craft.position.pos_z
        )

        craft_action = CraftAction(
            craft_subject= craft.craft_subject,
            amount=craft.craft_amount
        )

        action = Action(
            user=user,
            position=position,
            craft_action=craft_action
        )

        db.add(action)
        await db.commit()
        return {"status":"created"}

    except Exception as e:
        await db.rollback()
        logging.error(f"Error on handing craft action:{str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/kill")
async def add_kill(kill:KillNotification,user:CurrentUser,db:AsyncSession = Depends(get_db)):
    try:




        position = Position(
            pos_x=kill.position.pos_x,
            pos_y=kill.position.pos_y,
            pos_z=kill.position.pos_z
        )

        kill_action = KillAction(
            killed_type= kill.kill_type,
            kill_tool=kill.kill_tool,
            killed_subject_id= kill.kill_subject,
            killed_name= kill.kill_name
        )

        action = Action(
            user=user,
            position=position,
            kill_action=kill_action
        )

        db.add(action)
        await db.commit()
        return {"status": "created"}

    except Exception as e:
        await db.rollback()
        logging.error(f"Error on handing kill action:{str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/breed")
async def add_breed(breed:BreedNotification,user:CurrentUser,db:AsyncSession = Depends(get_db)):
    try:
        position = Position(
            pos_x=breed.position.pos_x,
            pos_y=breed.position.pos_y,
            pos_z=breed.position.pos_z
        )

        breed_action = BreedAction(
            father_subject_id=breed.father_subject_id,
            mother_subject_id=breed.mother_subject_id,
            child_subject_id=breed.child_subject_id,
            child_type=breed.child_type
        )

        action = Action(
            user=user,
            position=position,
            breed_action=breed_action
        )

        db.add(action)
        await db.commit()
        return {"status": "created"}

    except Exception as e:
        await db.rollback()
        logging.error(f"Error on handing breed action:{str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/death")
async def add_death(death:DeathNotification,user:CurrentUser,db:AsyncSession = Depends(get_db)):
    try:
        position = Position(
            pos_x=death.position.pos_x,
            pos_y=death.position.pos_y,
            pos_z=death.position.pos_z
        )

        death_action = DeathAction(
            death_cause=death.death_cause,
        )

        action = Action(
            user=user,
            position=position,
            death_action=death_action
        )

        db.add(action)
        await db.commit()
        return {"status": "created"}

    except Exception as e:
        await db.rollback()
        logging.error(f"Error on handing death action:{str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/pray")
async def add_pray(pray:PrayNotification,user:CurrentUser,db:AsyncSession = Depends(get_db)):
    try:

        position = Position(
            pos_x=pray.position.pos_x,
            pos_y=pray.position.pos_y,
            pos_z=pray.position.pos_z
        )

        pray_request = PrayResponseRequest(
            u= user.username,
            t= pray.pray_text,
            k= user.karma
        )

        pray_response = await get_pray_response(pray_request)

        pray_action = PrayAction(
            pray_text= pray.pray_text,
            pray_respond=pray_response
        )

        action = Action(
            user=user,
            position=position,
            pray_action=pray_action 
        )

        db.add(action)
        await db.commit()
        return JSONResponse(status_code=200, content={"pray_respond":pray_response})

    except Exception as e:
        await db.rollback()
        logging.error(f"Error on handing pray action:{str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
