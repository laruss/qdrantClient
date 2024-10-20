import os

from fastapi import APIRouter, UploadFile, Response, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from waiting import wait

from app.utils import cli, files
from app.utils.errors import NotFoundError, BadRequestError
from app.utils.logger import logger
from env import env

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.post('/face', operation_id="uploadFaceImage")
async def upload_face_image(file: UploadFile) -> Response:
    await files.save_image(file, env.FACE_IMAGE_PATH)

    return Response(status_code=204)


async def delete_files_after_merge():
    from asyncio import sleep
    await sleep(5)
    os.remove(env.MERGED_IMAGE_PATH)
    os.remove(env.DO_IMAGE_PATH)
    logger.info("Files removed")


@router.post('/test')
async def test(file: UploadFile) -> JSONResponse:
    return JSONResponse(
        content={
            "filename": file.filename,
            "contentType": file.content_type,
            "fileSize": file.size,
        }
    )


@router.get('/images/{file_name}', operation_id="getImage")
async def get_image(
        file_name: str,
        background_tasks: BackgroundTasks,
        merge_faces: bool = True,
):
    path = await files.download_from_do(
        do_filename=file_name,
        local_path=env.DO_IMAGE_PATH,
    )
    if not path:
        raise NotFoundError(f"File {file_name} not found in DigitalOcean")

    if merge_faces:
        if not os.path.exists(env.FACE_IMAGE_PATH):
            raise BadRequestError(f"Face image not found")

        res = cli.run_cli_command(
            env.CLI_MERGE_FACE_COMMAND.format(
                facefusion_path=env.FACEFUSION_PATH,
                face_image=env.FACE_IMAGE_PATH,
                do_image=env.DO_IMAGE_PATH,
                merged_image=env.MERGED_IMAGE_PATH,
            )
        )
        logger.info(res)

        path = env.MERGED_IMAGE_PATH

    wait(lambda: os.path.exists(path), timeout_seconds=5, waiting_for="file to be created")

    background_tasks.add_task(delete_files_after_merge)

    return FileResponse(path=path)
