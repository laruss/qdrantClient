from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

from app.utils.encoder import encoder
from app.utils.logger import logger
from app.models.image_description import ImageDescription
from env import env


"""
Little explanation:

We have a Qdrant class that is responsible for creating a collection, uploading points, and searching for points in the collection.

Vector size is calculated as the size of the sentence embedding multiplied by X, where X is the number of vectors we concatenate.

More vectors we concatenate, more information we have about the image, but it also increases the size of the vector and the time it takes to search for similar vectors and upload them.
"""


class Qdrant:
    client: QdrantClient
    encoder: SentenceTransformer
    collection: str = env.QDRANT_COLLECTION

    def __init__(self):
        self.client = QdrantClient(url=f'http://{env.QDRANT_HOST}:{env.QDRANT_PORT}')
        self.encoder = encoder.encoder
        logger.info(f"Qdrant client created: {self.client}")

    @property
    def __vector(self):
        return models.VectorParams(size=self.encoder.get_sentence_embedding_dimension(), distance=models.Distance.COSINE)

    def create_collection(self, delete: bool = False):
        """
        Create a collection in Qdrant

        Parameters:
            - delete: bool - whether to delete the collection before creating it

        Returns:
            - None
        """
        if delete:
            self.client.delete_collection(collection_name=self.collection)
            logger.info(f"Collection {self.collection} deleted")

        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config={
                    'description': self.__vector,
                    'setting': self.__vector,
                    'femaleDescription': self.__vector,
                    'femalePromiscuity': self.__vector,
                    'places': self.__vector,
                },
            )
            logger.info(f"Collection {self.collection} created")
        else:
            logger.info(f"Collection {self.collection} already exists")

    def upload_points(self, data: dict[str, ImageDescription]):
        """
        Upload points to the collection

        Parameters:
            - data: dict[str, ImageDescription] - dictionary of ImageDescription objects

        Returns:
            - None
        """
        self.client.upload_points(
            collection_name=self.collection,
            points=[
                models.PointStruct(
                    id=idx,
                    vector=item[1].get_as_vector(),
                    payload={
                        "item": item[1].model_dump(),
                        "file_name": item[0],
                    },
                )
                for idx, item in enumerate(data.items())
            ]
        )
        logger.info(f"Points uploaded to collection {self.collection}")

    def search(self, query: ImageDescription, limit: int = 5) -> list[models.ScoredPoint]:
        """
        Search for similar vectors in the collection

        Parameters:
            - query: ImageDescription - ImageDescription object
            - limit: int - number of similar vectors to return

        Returns:
            - list[models.ScoredPoint] - list of similar vectors
        """
        return self.client.query_points(
            collection_name=self.collection,
            prefetch=[
                models.Prefetch(
                    query=query.get_as_vector()['description'],
                    using='description',
                ),
                models.Prefetch(
                    query=query.get_as_vector()['setting'],
                    using='setting',
                ),
                models.Prefetch(
                    query=query.get_as_vector()['femaleDescription'],
                    using='femaleDescription',
                ),
                models.Prefetch(
                    query=query.get_as_vector()['femalePromiscuity'],
                    using='femalePromiscuity',
                ),
                models.Prefetch(
                    query=query.get_as_vector()['places'],
                    using='places',
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.DBSF),
            limit=limit,
        ).points
