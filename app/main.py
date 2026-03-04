from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
#    await drop_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

