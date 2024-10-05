from aioboto3 import Session

from env import env
from app.utils.logger import logger


class DigitalOcean:
    space_name: str = env.DOP_SPACE_NAME

    def __init__(self):
        ses = Session()
        self.client = ses.client(
            's3',
                        endpoint_url=f'https://{env.DOP_SPACE_REGION}.digitaloceanspaces.com',
                        aws_access_key_id=env.DOP_SPACE_PUBLIC_ACCESS_KEY,
                        aws_secret_access_key=env.DOP_SPACE_PRIVATE_API_KEY
        )

    @staticmethod
    def log(msg):
        logger.info(f"DO: {msg}")

    async def upload_file(self, local_path: str, remote_path: str):
        """
        Upload a file to your Space

        :param local_path: str, path to the file on your local machine (e.g. 'C:/Users/you/test.html')
        :param remote_path: str, path to the file in your Space (e.g. 'media/new_file_name.html')
        :return: None
        """
        async with self.client as s3:
            await s3.upload_file(local_path, self.space_name, remote_path)

        self.log(f"File uploaded to {remote_path}")

    async def download_file(self, local_path: str, remote_path: str):
        """
        Download a file from your Space

        :param local_path: str, path to save the file on your local machine (e.g. 'C:/Users/you/test.html')
        :param remote_path: str, path to the file in your Space (e.g. 'media/new_file_name.html')
        :return: None
        """
        async with self.client as s3:
            await s3.download_file(self.space_name, remote_path, local_path)

        self.log(f"File downloaded to {local_path}")

    async def delete_file(self, remote_path: str):
        """
        Delete a file from your Space

        :param remote_path: str, path to the file in your Space (e.g. 'media/new_file_name.html')
        :return: None
        """
        async with self.client as s3:
            await s3.delete_object(Bucket=self.space_name, Key=remote_path)

        self.log(f"File deleted from {remote_path}")

    async def is_file_exists(self, remote_path: str) -> bool:
        """
        Check if a file exists in your Space

        :param remote_path: str, path to the file in your Space (e.g. 'media/new_file_name.html')
        :return: bool
        """
        try:
            async with self.client as s3:
                await s3.head_object(Bucket=self.space_name, Key=remote_path)
            return True
        except self.client.exceptions.ClientError:
            return False

    async def get_list_of_files(self, remote_folder_path: str) -> list[str]:
        """
        Get a list of all files in your Space

        :param remote_folder_path: str, path to the folder in your Space (e.g. 'media/')
        :return: list[str]
        """
        async with self.client as s3:
            response = await s3.list_objects(Bucket=self.space_name, Prefix=remote_folder_path)
            files = [obj['Key'] for obj in response.get('Contents', [])]
            self.log(f"Got a list of files: {files}")
            del files[0]

        return [file.replace(remote_folder_path, '') for file in files]
