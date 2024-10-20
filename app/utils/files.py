import io
import os
import uuid

import cloudscraper
import imagehash
from PIL import Image
from fastapi import UploadFile

from app.utils.errors import BadRequestError, ApplicationError
from app.services.digital_ocean import DigitalOcean
from app.utils.logger import logger
from env import env


async def verify_image(file: UploadFile) -> Image.Image:
    """
    Verify that the file is an image.

    Parameters:
        - file: UploadFile - file object

    Returns:
        - Image.Image - PIL image object
    """

    file_content = await file.read()
    try:
        image = Image.open(io.BytesIO(file_content))
        image.verify()
        return Image.open(io.BytesIO(file_content))
    except (IOError, SyntaxError) as e:
        raise BadRequestError(f"File {file.filename} is not an image: {e}")


async def save_image(file: UploadFile, path: str) -> str:
    """
    Save image to path.

    Parameters:
        - file: UploadFile - file object
        - path: str - full path to save the file (e.g. '/path/to/file_name.ext')

    Returns:
        - str - path to the saved file
    """
    image = await verify_image(file)
    image.save(path, format="PNG")

    return path


def to_webp(image_bytes: bytes = None, image_path: str = None, max_size_in_kb: int = 500) -> bytes:
    """
    Convert image to WEBP format

    Parameters:
        - image_bytes: bytes - image bytes
        - image_path: str - path to the image
        - max_size_in_kb: int - maximum size of the image in KB

    Returns:
        - bytes - converted image bytes
    """
    with Image.open(io.BytesIO(image_bytes) if image_bytes else image_path) as img:
        output = io.BytesIO()

        quality = 80
        img.save(output, format="WEBP", quality=quality)

        while output.tell() > max_size_in_kb * 1024:
            quality -= 10
            if quality < 10:
                break
            output.seek(0)
            output.truncate(0)
            img.save(output, format="WEBP", quality=quality)

        webp_image_bytes = output.getvalue()
        output.close()

        return webp_image_bytes


def download_from_url(url: str, file_path: str) -> str:
    session = cloudscraper.create_scraper()
    try:
        response = session.head(url, timeout=60)
    except Exception as e:
        raise ApplicationError(f"Error downloading image: {e}")
    try:
        response.raise_for_status()
    except Exception as e:
        raise ApplicationError(f"Error downloading image: {e}")

    mime_type = response.headers.get('Content-Type')

    if mime_type not in ('image/png', 'image/jpeg', 'image/webp'):
        raise ApplicationError(f"Unsupported image format: {mime_type}")

    try:
        response = session.get(url, stream=True, timeout=60)
        response.raise_for_status()
    except Exception as e:
        raise ApplicationError(f"Error downloading image: {e}")

    image_bytes = io.BytesIO()
    for chunk in response.iter_content(1024):
        image_bytes.write(chunk)

    try:
        webp_image_bytes = to_webp(image_bytes.getvalue(), max_size_in_kb=600)
    except Exception as e:
        logger.warning(f"Error processing image: {e}")
        raise ApplicationError(f"Image conversion to WebP failed: {e}")

    with open(file_path, 'wb') as file:
        file.write(webp_image_bytes)

    try:
        Image.open(file_path).verify()
    except Exception as e:
        os.remove(file_path)
        logger.warning(f"Error verifying file: {e}")
        raise ApplicationError(f"Image is corrupted")

    return file_path


async def upload_to_do(image_name: str, path: str) -> str:
    """
    Upload image to Digital Ocean

    Parameters:
        - file_type: ImageType (see ImageType enum)
        - image_name: str - name of the image that will be used in the DO
        - path: optional str - path to the local image file

    Returns:
        - str - remote path to the uploaded image (e.g. 'lm_game/main_characters/image_name')
    """
    do = DigitalOcean()
    if not os.path.exists(path):
        raise ApplicationError(f"File {path} not found")

    remote_path = env.DOP_PATH + image_name

    await do.upload_file(local_path=path, remote_path=remote_path)

    return remote_path


async def download_from_do(do_filename: str, local_path: str) -> str | None:
    """
    Download a file from Digital Ocean

    Parameters:
        - do_filename: str - file name in DigitalOcean without path (e.g. 'file_name.ext')
        - local_path: str - path to save the file on your local machine (e.g. 'C:/Users/you/test.html')

    Returns:
        - str | None; None if the file does not exist, otherwise the local path to the downloaded file
    """
    do = DigitalOcean()
    do_path = env.DOP_PATH + do_filename
    try:
        await do.download_file(local_path=local_path, remote_path=do_path)
    except Exception as e:
        return None

    return local_path


async def delete_in_do(file_name: str):
    """
    Delete file from DigitalOcean.

    Parameters:
        - file_name: str - file name in DigitalOcean without path (e.g. 'file_name.ext')

    Returns:
        - None
    """
    await DigitalOcean().delete_file(f"{env.DOP_PATH}{file_name}")



def get_file_hash(path: str) -> str:
    image = Image.open(path)
    hash_ = imagehash.phash(image)

    return str(hash_)


def get_unique_filename(ext: str = 'webp') -> str:
    return f"{str(uuid.uuid4()).split('-')[-1]}.{ext}"


def delete_all_files_in_folder(folder_path: str, exclude: list[str] = None):
    """
    Delete all files in the folder except the ones in the exclude list.

    Parameters:
        - folder_path: str - path to the folder
        - exclude: list[str] - list of file names to exclude from deletion
    """
    for file_name in os.listdir(folder_path):
        if exclude and (file_name in exclude or folder_path + file_name in exclude):
            logger.info(f"File {file_name} excluded from deletion")
            continue

        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
        logger.info(f"File {file_path} removed")
