import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from app.utils.logger import logger
from env import env
from utils.qdrant_uploader.types import ImageDataWithVectors


class QdrantService:
    client: QdrantClient
    collection: str = env.QDRANT_COLLECTION

    def __init__(self):
        self.client = QdrantClient(
            url=env.QDRANT_CLOUD_API_URL,
            api_key=env.QDRANT_CLOUD_API_KEY,
        )

    def count(self):
        return self.client.count(collection_name=self.collection)

    def create_collection_if_not_exists(self, delete: bool = False):
        if delete:
            self.client.delete_collection(collection_name=self.collection)
            logger.info(f"Collection `{self.collection}` deleted")

        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=dict(
                    image_vector=VectorParams(size=512, distance=Distance.COSINE),
                    description_vector=VectorParams(size=512, distance=Distance.COSINE),
                ),
            )
            logger.info(f"Collection `{self.collection}` created")
        else:
            logger.info(f"Collection `{self.collection}` already exists")

    def upload_points(self, *data: ImageDataWithVectors):
        self.client.upload_points(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=uuid.uuid4().hex,
                    vector={"image_vector": d.image_vector},
                    payload=dict(
                        image_url=d.image_url,
                        description=d.description,
                    ),
                ) for d in data
            ]
        )
        results_all = self.client.count(collection_name=self.collection)
        logger.info(f"Uploaded {len(data)} points to collection `{self.collection}`. Total points: {results_all}")

    def update_point(self, id: str, data: ImageDataWithVectors):
        point = PointStruct(
            id=id,
            vector=dict(
                image_vector=data.image_vector,
                description_vector=data.description_vector,
            ),
            payload=dict(
                image_url=data.image_url,
                description=data.description,
            ),
        )
        self.client.upsert(collection_name=self.collection, points=[point])

    def search(self, query_vector: list[float], top_k: int = 10):
        results_all = self.client.count(collection_name=self.collection)
        print(results_all)

        results_image = self.client.search(
            collection_name=self.collection,
            query_vector=("image_vector", query_vector),
            limit=top_k,
            with_payload=True
        )
        print(len(results_image))

        results_description = self.client.search(
            collection_name=self.collection,
            query_vector=("description_vector", query_vector),
            limit=top_k,
            with_payload=True
        )
        print(len(results_description))

        # United results
        combined_results = results_image + results_description

        # Delete duplicates by id
        unique_results = {}
        for result in combined_results:
            if result.id not in unique_results:
                unique_results[result.id] = result
            else:
                # If the result with the same id has a higher score, replace it
                if result.score > unique_results[result.id].score:
                    unique_results[result.id] = result

        # Sort by score
        final_results = sorted(unique_results.values(), key=lambda x: x.score, reverse=True)

        # Return top k results
        final_results = final_results[:top_k]

        return final_results
