from .config import router as config_router
from .data import router as data_router
from .describe import router as describe_router
from .files import router as files_router
from .media import router as media_router
from .search import router as search_router


routers = [
    config_router,
    data_router,
    describe_router,
    files_router,
    media_router,
    search_router,
]
