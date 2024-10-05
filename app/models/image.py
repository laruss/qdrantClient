from datetime import datetime

from pydantic import BaseModel

from app.models.base_db import BaseDb
from app.models.image_description import ImageDescription


class ImageValidator(BaseModel):
    file_name: str
    description: ImageDescription | None = None
    hash: None | str = None
    created_at: datetime | None = datetime.now()


class ImageModel(BaseDb[ImageValidator]):
    Validator = ImageValidator
    __mongo_collection__ = BaseDb.db["images"]
