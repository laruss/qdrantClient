import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.errors import BadRequestError, NotFoundError, ApplicationError
from app.services.qdrant import Qdrant
from env import env

from app.routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.qdrant = Qdrant()
    if not os.path.exists(env.TEMP_DIR):
        os.makedirs(env.TEMP_DIR)
    yield

app = FastAPI(
    title=env.APP_NAME,
    version=env.APP_VERSION,
    lifespan=lifespan,
)


for router in routers:
    app.include_router(router)


@app.get("/")
async def read_root():
    return {"message": "Application is running"}


@app.exception_handler(BadRequestError)
async def bad_request_exception_handler(_, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"message": exc.message})


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(_, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": exc.message})


@app.exception_handler(ApplicationError)
async def application_exception_handler(_, exc: ApplicationError):
    return JSONResponse(status_code=500, content={"message": exc.message})
