import json
import os

from fastapi import APIRouter, UploadFile, Response, BackgroundTasks
from fastapi.responses import FileResponse

from waiting import wait

from app import files, cli
from app.annotations import AnnotatedQdrant
from app.errors import NotFoundError, BadRequestError
from app.logger import logger
from app.models import ImageDescription
from env import env

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.post('/data', operation_id="uploadDataFile")
async def upload_data_file(
        file: UploadFile,
        qdrant: AnnotatedQdrant,
):
    res = await file.read()
    res_dict = json.loads(res)

    described_dict: dict[str, ImageDescription] = {}

    for key, value in res_dict.items():
        if desc := value.get("description"):
            described_dict[key] = ImageDescription(**desc)

    qdrant.create_collection(True)
    qdrant.upload_points(described_dict)

    return {
        "status": "ok",
        "uploaded": len(described_dict),
    }


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


@router.get('/images/{file_name}', operation_id="getImage")
async def get_image(
        file_name: str,
        background_tasks: BackgroundTasks,
        merge_faces: bool = True,
):
    path = await files.download_from_do(
        do_path=f"{env.DOP_PATH}{file_name}",
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
