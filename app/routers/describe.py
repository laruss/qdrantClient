from fastapi import APIRouter, Response

from pydantic import BaseModel

from app.annotations import AnnotatedCurrentMediaInfo
from app.models.image import ImageModel
from app.models.image_description import ImageDescription
from app.services.anthropic_service import Anthropic
from app.utils.errors import NotFoundError
from env import env

router = APIRouter(
    prefix="/description",
    tags=["description"],
    responses={404: {"description": "Not found"}},
)

anthropic = Anthropic()


@router.get("", operation_id="getDescription")
async def get_description(info: AnnotatedCurrentMediaInfo) -> ImageDescription:
    if not info:
        raise NotFoundError("No current media")

    if info.description:
        return info.description

    return ImageDescription(
        description="",
        setting="",
        femaleDescription="",
        femalePromiscuity="",
        places=[],
        hashtags=[],
    )


@router.post("", operation_id="setDescription")
async def set_description(info: AnnotatedCurrentMediaInfo, description: ImageDescription):
    if not info:
        raise NotFoundError("No current media")
    info.description = description
    await ImageModel.update_one(info, file_name=info.file_name)

    return Response(status_code=204)


class DescribeMediaPayload(BaseModel):
    prompt: str = ''


@router.post("/describe", operation_id="describeMedia", status_code=204)
async def describe_media(
        info: AnnotatedCurrentMediaInfo,
        data: DescribeMediaPayload,
):
    res = await anthropic.describe_image(data.prompt, image_path=env.TEMP_DIR + info.file_name)
    info.description = res
    await ImageModel.update_one(info, file_name=info.file_name)

    return Response(status_code=204)
