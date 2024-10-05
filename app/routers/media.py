import os
import shutil
from typing import Literal

from fastapi import APIRouter, Response, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.annotations import AnnotatedCurrentMediaInfo, AnnotatedConfig, AnnotatedAllForCurrentDataType, \
    AnnotatedHashesData, AnnotatedQdrant
from app.models.config import ConfigValidator, ConfigModel
from app.models.image import ImageValidator, ImageModel
from app.services.yandex import yandex
from app.utils import files
from app.utils.errors import NotFoundError, ApplicationError, BadRequestError
from app.utils.logger import logger
from env import env

router = APIRouter(
    prefix="/media",
    tags=["media"],
    responses={404: {"description": "Not found"}},
)


@router.get("/current/data",
            operation_id="getCurrentMediaData",
            response_model=ImageValidator,
            response_model_exclude={"hash"},
            )
async def get_current_media_data(info: AnnotatedCurrentMediaInfo):
    if info is None:
        raise NotFoundError("No current media")

    return info


def get_next_previous_media(
        config_: ConfigValidator,
        all_media: list[ImageValidator],
        direction: Literal['next', 'prev']
):
    if config_.currentMedia is None:
        return all_media[0]

    current_media_index = next((i for i, x in enumerate(all_media) if x.file_name == config_.currentMedia), None)
    if current_media_index is None:
        raise ApplicationError("Something went wrong, current media not found")

    if direction == 'next':
        next_media = all_media[(current_media_index + 1) % len(all_media)]
    elif direction == 'prev':
        next_media = all_media[(current_media_index - 1) % len(all_media)]
    else:
        raise ApplicationError("Invalid direction")

    # delete temp duplicates folder because it's not needed
    if os.path.exists(env.TEMP_DUPLICATES_PATH):
        shutil.rmtree(env.TEMP_DUPLICATES_PATH)

    return next_media


@router.post("/next", operation_id="setNextMedia")
async def set_next_media(
        all_media: AnnotatedAllForCurrentDataType,
        config_: AnnotatedConfig,
        info: AnnotatedCurrentMediaInfo,
        qdrant: AnnotatedQdrant,
):
    # save current media to qdrant if it is described
    if info.description:
        qdrant.upload_points({info.file_name: info.description})

    next_media = get_next_previous_media(config_, all_media, 'next')

    await ConfigModel.set_current_media(next_media.file_name)

    return Response(status_code=204)


@router.post("/previous", operation_id="setPreviousMedia")
async def set_previous_media(
        config_: AnnotatedConfig,
        all_media: AnnotatedAllForCurrentDataType
):
    prev_media = get_next_previous_media(config_, all_media, 'prev')

    await ConfigModel.set_current_media(prev_media.file_name)

    return Response(status_code=204)


@router.get("/current", operation_id="getMedia")
async def get_media(config_: AnnotatedConfig) -> FileResponse:
    if not config_.currentMedia:
        raise NotFoundError("No current media")

    if os.path.exists(env.TEMP_DIR + config_.currentMedia):
        return FileResponse(env.TEMP_DIR + config_.currentMedia, media_type="image/webp")

    local_path = await files.download_from_do(
        do_filename=config_.currentMedia, local_path=env.TEMP_DIR + config_.currentMedia
    )
    return FileResponse(local_path, media_type="image/webp")


class AlikeImage(BaseModel):
    url: str
    width: int
    height: int


class GetAlikeMediaResponse(BaseModel):
    images: list[list[AlikeImage]]


@router.get("/alike", operation_id="getAlikeMedia")
def get_alike_media(config_: AnnotatedConfig) -> GetAlikeMediaResponse:
    full_path = env.TEMP_DIR + config_.currentMedia
    images_ = yandex.get_similar_images(full_path)

    response = GetAlikeMediaResponse(images=[])
    for image in images_:
        response.images.append(
            [AlikeImage(url=img.url, width=img.w, height=img.h) for img in image.preview]
        )

    return response


class DownloadAlikeMediaBody(BaseModel):
    url: str


async def check_image_hash_and_upload_to_do(
        filename: str,
        file_path: str,
        hashes: list[str],
) -> Response:
    file_hash = files.get_file_hash(file_path)
    if file_hash in hashes:
        os.remove(file_path)
        raise BadRequestError("Image already exists")

    await files.upload_to_do(filename, file_path)
    logger.info(f'Image {filename} successfully uploaded to DigitalOcean')
    await ImageModel.insert_one(ImageValidator(file_name=filename, hash=file_hash))
    logger.info(f'Image {filename} successfully saved to database')

    hashes.append(file_hash)

    return Response(status_code=204)


@router.post("/alike/download", operation_id="downloadAlikeMedia")
async def download_alike_media(
        body: DownloadAlikeMediaBody,
        hashes: AnnotatedHashesData
):
    filename = files.get_unique_filename()  # '<some_hash>.webp'
    file_path = files.download_from_url(body.url, env.TEMP_DIR + filename)

    return await check_image_hash_and_upload_to_do(filename, file_path, hashes)


@router.post("/upload")
async def upload_media(
        file: UploadFile,
        hashes: AnnotatedHashesData
):
    filename = files.get_unique_filename()
    file_path = await files.save_image(file, env.TEMP_DIR + filename)

    return await check_image_hash_and_upload_to_do(filename, file_path, hashes)


@router.delete("/text", operation_id="removeTextFromImage", deprecated=True)
async def remove_text_from_image():
    # https://github.com/liawifelix/auto-text-removal
    return {"info": "Deprecated endpoint"}


@router.delete('', operation_id='deleteMedia', status_code=204)
async def delete_media(config_: AnnotatedConfig, all_media: AnnotatedAllForCurrentDataType):
    if not config_.currentMedia:
        raise NotFoundError("No current media")

    next_media = get_next_previous_media(config_, all_media, 'next')

    await files.delete_in_do(file_name=config_.currentMedia)
    await ImageModel.delete_one(file_name=config_.currentMedia)
    await ConfigModel.set_current_media(next_media.file_name)

    return Response(status_code=204)

