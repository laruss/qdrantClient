import json
from typing import Any

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.annotations import AnnotatedQdrant
from app.models.image import ImageValidator, ImageModel
from app.models.image_description import ImageDescription
from utils.vecotizer.vecorizer import get_image_vector

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
        upload_in_qdrant: bool = True,
        delete_existing: bool = False,
):
    json_content = json.loads(await file.read())
    payload = UploadImageDataPayload.model_validate({"data": json_content})
    if delete_existing:
        await ImageModel.delete_all()

    for file_name, data in payload.data.items():
        await ImageModel.insert_one(
            ImageValidator(
                file_name=file_name,
                hash=data.hash,
                description=data.description,
            )
        )

    if upload_in_qdrant:
        described_dict: dict[str, ImageDescription] = {}
        for key, value in json_content.items():
            if desc := value.get("description"):
                described_dict[key] = ImageDescription(**desc)
        qdrant.create_collection(delete=True)
        qdrant.upload_points(described_dict)

    return JSONResponse(content={"message": "Successfully saved data for images."})


class VectorizedResult(BaseModel):
    url: str
    vector: list[Any]


@router.get('/vectorize', operation_id="vectorizeImages")
async def vectorize_images(url: str) -> VectorizedResult:
    result = get_image_vector(url, None)
    # ndarray to list
    result = result.tolist()

    return VectorizedResult(url=url, vector=result)
