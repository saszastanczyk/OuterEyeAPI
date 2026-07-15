import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from App.routes import scan_notification,actions_notification,analysis_requests




@asynccontextmanager
async def lifespan(app:FastAPI):
    logging.level = logging.DEBUG
    logging.info("Started lifespan")
    yield
    logging.info("Ended lifecycle")

app = FastAPI(lifespan=lifespan)

app.include_router(scan_notification.router)
app.include_router(actions_notification.router)

app.include_router(analysis_requests.router)


