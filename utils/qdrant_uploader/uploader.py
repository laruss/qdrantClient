from utils.qdrant_uploader.qdrant import QdrantService
from utils.qdrant_uploader.types import ImageDataWithVectors

qdrant = QdrantService()
print(qdrant.count())

# # init data
# qdrant.create_collection_if_not_exists(True)
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

# # search data
# text = "3d"
# data = get_vector(None, text)
# print(data)
# search_vector = data["vector"][0]
# print(f"Searching for text `{text}`...")
# results = qdrant.search(search_vector, 1)
# print(results)
