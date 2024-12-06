from aioboto3 import Session

from app.utils.logger import logger
from env import env

class Backblaze:
    def __init__(self):
        self.session = Session(
            aws_access_key_id=env.BACKBLAZE_KEY_ID,
            aws_secret_access_key=env.BACKBLAZE_APPLICATION_KEY,
        )
        self.bucket = env.BACKBLAZE_BUCKET_NAME
        self.endpoint = env.BACKBLAZE_ENDPOINT

    async def upload_file(self, local_path: str, remote_path: str) -> str:
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint,
        ) as s3:
            await s3.upload_file(local_path, self.bucket, remote_path)

        logger.info(f"File uploaded to {remote_path}")
        return remote_path

    async def download_file(self, local_path: str, remote_path: str) -> str:
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint,
        ) as s3:
            await s3.download_file(self.bucket, remote_path, local_path)

        logger.info(f"File downloaded to {local_path}")

    async def delete_file(self, remote_path: str):
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint,
        ) as s3:
            await s3.delete_object(Bucket=self.bucket, Key=remote_path)

        logger.info(f"File deleted from {remote_path}")
