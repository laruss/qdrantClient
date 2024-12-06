import requests

from utils.qdrant_uploader.qdrant import QdrantService
from utils.qdrant_uploader.types import ImageDataWithVectors

# image_links = [
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395740/cld-sample-5.jpg",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395740/cld-sample-4.jpg",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395740/cld-sample-2.jpg",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395740/cld-sample.jpg",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395740/cld-sample-3.jpg",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395740/samples/logo.png",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395739/samples/woman-on-a-football-field.jpg",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395739/samples/dessert-on-a-plate.jpg",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395739/samples/upscale-face-1.jpg",
#     "http://res.cloudinary.com/dtlkjt5wh/image/upload/v1733395739/samples/cup-on-a-table.jpg"
# ]

# erotic images
image_links = [
    "https://cf.girlsaskguys.com/q3815192/150b8124-668d-4698-ba93-ab454f6ed764.jpg",
    "https://i.pinimg.com/736x/72/73/65/7273650e4b134413da1c82e4a509efb8.jpg",
    "https://media.glamourmagazine.co.uk/photos/66155a28862c087fad320c35/2:3/w_852,h_1278,c_limit/best%20bikinis%20for%20small%20boobs%20090424%20SCREENSHOT%202024-04-09%20AT%2016.05.12%20COPY%202.jpg",
    "https://i.ebayimg.com/images/g/UJEAAOSwkvhkpBXT/s-l400.jpg",
    "https://p.turbosquid.com/ts-thumb/Jn/EYQmMR/wT/b_0001/png/1656384161/600x600/fit_q87/4ab04c942e0baaf67d94de2f4bd6657f9a36aa4c/b_0001.jpg",
    "https://img5.hotnessrater.com/6652916/sydney-sweeney-topless.jpg"
]

qdrant = QdrantService()
session = requests.Session()
session.auth = ('konstantin', '3752860941YaKIm')
url = "https://faceswap.a.pinggy.link/data/vectorize"


def get_vector(img: str | None, description: str | None) -> dict:
    return session.get(
        url, params={"url": img, "text": description}
    ).json()


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

# search data
text = "3d"
data = get_vector(None, text)
print(data)
search_vector = data["vector"][0]
print(f"Searching for text `{text}`...")
results = qdrant.search(search_vector, 1)
print(results)
