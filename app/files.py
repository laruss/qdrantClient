import io

from PIL import Image
from fastapi import UploadFile

from app.errors import BadRequestError
from app.services.digital_ocean import DigitalOcean


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


async def download_from_do(do_path: str, local_path: str) -> str | None:
    """
    Download a file from Digital Ocean

    Parameters:
        - do_path: str - path to the file in your Space (e.g. 'media/new_file_name.html')
        - local_path: str - path to save the file on your local machine (e.g. 'C:/Users/you/test.html')

    Returns:
        - str | None; None if the file does not exist, otherwise the local path to the downloaded file
    """
    do = DigitalOcean()
    try:
        await do.download_file(local_path, do_path)
    except do.client.exceptions.ClientError:
        return None

    return local_path
