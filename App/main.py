import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.params import Depends

from src.Database import get_db


@asynccontextmanager
async def lifespan(app:FastAPI):
    logging.level = logging.DEBUG
    logging.info("Started lifespan")
    yield
    logging.info("Ended lifecycle")

app = FastAPI(lifespan=lifespan)





