from typing import Annotated
from fastapi import Request, Depends

from app.services.qdrant import Qdrant


async def get_qdrant(request: Request):
    return request.app.qdrant


AnnotatedQdrant = Annotated[Qdrant, Depends(get_qdrant)]
