from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.crud import router as crud_router

import app.models
from app.db import create_tables, drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
#    await drop_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(crud_router)