from fastapi import APIRouter
from pydantic import BaseModel

from app.annotations import AnnotatedQdrant
from app.models.image_description import ImageDescription

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)


class SearchResponse(BaseModel):
    results: dict[str, ImageDescription]


@router.post("", operation_id="search")
async def search(
        qdrant: AnnotatedQdrant,
        payload: ImageDescription,
        limit: int | None = 5,
) -> SearchResponse:
    limit = limit or 5
    res = qdrant.search(payload, limit=limit)
    items: dict[str, ImageDescription] = {}
    for item in res:
        items[item.payload['file_name']] = item.payload['item']

    return SearchResponse(results=items)
