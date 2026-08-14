import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routes import scan_notification,actions_notification,analysis_requests

@asynccontextmanager
async def lifespan(app:FastAPI):
    logging.info("Started lifecycle")
    yield
    logging.info("Ended lifecycle")

app = FastAPI(lifespan=lifespan)

app.include_router(scan_notification.router)
app.include_router(actions_notification.router)

app.include_router(analysis_requests.router)


