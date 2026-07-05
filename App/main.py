import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from routes import scan




@asynccontextmanager
async def lifespan(app:FastAPI):
    logging.level = logging.INFO
    logging.info("Started lifespan")
    yield
    logging.info("Ended lifecycle")

app = FastAPI(lifespan=lifespan)

app.include_router(scan.router)



