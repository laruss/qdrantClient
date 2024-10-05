import json

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.annotations import AnnotatedQdrant
from app.models.image import ImageValidator, ImageModel
from app.models.image_description import ImageDescription

router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


@router.get("", operation_id="downloadAllImagesData")
async def download_all_images_data():
    all_existing_media: list[ImageValidator] = await ImageModel.get_many()
    images_data = {
        media.file_name: {
            "hash": media.hash, "description": media.description.model_dump() if media.description else None,
        } for media in all_existing_media
    }

    return JSONResponse(content=images_data)


class ImageData(BaseModel):
    hash: str
    description: ImageDescription | None = None


class UploadImageDataPayload(BaseModel):
    data: dict[str, ImageData]


@router.post("", operation_id="uploadImageData")
async def upload_image_data(
        file: UploadFile,
        qdrant: AnnotatedQdrant,
        uploadInQdrant: bool = True,
):
    json_content = json.loads(await file.read())
    payload = UploadImageDataPayload.model_validate({"data": json_content})
    for file_name, data in payload.data.items():
        await ImageModel.insert_one(
            ImageValidator(
                file_name=file_name,
                hash=data.hash,
                description=data.description,
            )
        )

    if uploadInQdrant:
        described_dict: dict[str, ImageDescription] = {}
        for key, value in json_content.items():
            if desc := value.get("description"):
                described_dict[key] = ImageDescription(**desc)
        qdrant.create_collection(True)
        qdrant.upload_points(described_dict)

    return JSONResponse(content={"message": "Successfully saved data for images."})
