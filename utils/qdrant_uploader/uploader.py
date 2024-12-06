import requests

from utils.qdrant_uploader.qdrant import QdrantService
from utils.qdrant_uploader.types import ImageDataWithVectors




def get_vector(img: str | None, description: str | None) -> dict:
    return session.get(
        url, params={"url": img, "description": description}
    ).json()

# # init data
# qdrant.create_collection_if_not_exists()
#
# for link in image_links:
#     # 1. send vectorize request via API
#     data = get_vector(link, None)
#     print(data)
#     image_data = ImageDataWithVectors(
#         image_url=link,
#         description=None,
#         image_vector=data["vector"][0],
#         description_vector=[],
#     )
#     # 2. upload to qdrant
#     qdrant.upload_points(image_data)
#
# print("Done")


# search data
# data = get_vector(None, "white mountains")
# print(data)
