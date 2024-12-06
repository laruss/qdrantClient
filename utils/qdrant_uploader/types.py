from pydantic import BaseModel


class ImageDataWithVectors(BaseModel):
    image_url: str
    image_vector: list[float]
    description: str | None = None
    description_vector: list[float] = []
