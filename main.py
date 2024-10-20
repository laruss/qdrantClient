import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.routers.config import create_config_if_not_exists
from app.utils import files
from app.utils.errors import BadRequestError, NotFoundError, ApplicationError
from app.services.qdrant import Qdrant
from env import env

from app.routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.qdrant = Qdrant()
    await create_config_if_not_exists()
    files.delete_all_files_in_folder(env.TEMP_DIR, exclude=[env.FACE_IMAGE_PATH])

    if not os.path.exists(env.TEMP_DIR):
        os.makedirs(env.TEMP_DIR)

    yield

app = FastAPI(
    title=env.APP_NAME,
    version=env.APP_VERSION,
    lifespan=lifespan,
)


@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


for router in routers:
    app.include_router(router)


@app.exception_handler(BadRequestError)
async def bad_request_exception_handler(_, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"message": exc.message})


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(_, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": exc.message})


@app.exception_handler(ApplicationError)
async def application_exception_handler(_, exc: ApplicationError):
    return JSONResponse(status_code=500, content={"message": exc.message})


app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
