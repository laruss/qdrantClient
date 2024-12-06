import os
import json
import glob
import asyncio
from typing import List

# Constant: path to images catalog
IMAGES_CATALOG_PATH = "path/to/images"

from utils.backblaze_service.backblaze import Backblaze
from utils.vecotizer.vecorizer import get_image_vector
from utils.qdrant_uploader.qdrant import QdrantService
from utils.qdrant_uploader.types import ImageDataWithVectors

FILES_LIMIT = 10

# Note: All logging and comments in English.
# This script uploads images to Backblaze and Qdrant asynchronously.
# Steps per image:
# 1. Check if image is already uploaded (check uploaded.json).
# 2. If not, upload to Backblaze.
# 3. Vectorize image.
# 4. Upload vector to Qdrant.
# 5. Mark as uploaded in uploaded.json immediately after successful upload.

backblaze = Backblaze()
qdrant = QdrantService()
qdrant.create_collection_if_not_exists()

async def mark_as_uploaded(uploaded_json_path: str, uploaded_set: set, image_name: str):
    # Add image name to uploaded set and write to JSON file
    uploaded_set.add(image_name)
    # Write updated set to file
    with open(uploaded_json_path, "w") as f:
        json.dump(list(uploaded_set), f, indent=2)
    print(f"[INFO] {image_name} marked as uploaded and uploaded.json updated.")


async def process_image(
    image_path: str,
    uploaded_set: set,
    semaphore: asyncio.Semaphore,
    uploaded_json_path: str
) -> bool:
    """
    Process a single image file.
    Return True if successfully processed, False otherwise.
    """
    async with semaphore:
        image_name = os.path.basename(image_path)

        if image_name in uploaded_set:
            print(f"[INFO] {image_name} is already uploaded. Skipping.")
            return False

        print(f"[INFO] Processing image: {image_name}")

        # 1. Upload image to Backblaze
        try:
            await backblaze.upload_file(image_path, image_name)
        except Exception as e:
            print(f"[ERROR] Failed to upload {image_name} to Backblaze: {e}")
            return False

        print(f"[INFO] {image_name} uploaded to Backblaze.")

        # 2. Vectorize image
        try:
            vector_result = get_image_vector(None, image_path)
            if not vector_result or not isinstance(vector_result, list) or not vector_result[0]:
                print(f"[ERROR] Failed to vectorize {image_name}.")
                return False
            vector = vector_result[0]
        except Exception as e:
            print(f"[ERROR] Exception while vectorizing {image_name}: {e}")
            return False

        print(f"[INFO] {image_name} vectorized successfully.")

        # 3. Upload vector to Qdrant
        data = [ImageDataWithVectors(
            image_url=image_name,
            image_vector=vector,
            description=None,
            description_vector=[]
        )]

        try:
            qdrant.upload_points(*data)
        except Exception as e:
            print(f"[ERROR] Failed to upload vector of {image_name} to Qdrant: {e}")
            return False

        print(f"[INFO] {image_name} vector uploaded to Qdrant.")

        # 4. Mark as uploaded immediately
        await mark_as_uploaded(uploaded_json_path, uploaded_set, image_name)

        return True


async def main():
    # Load or create uploaded.json
    uploaded_json_path = os.path.join(IMAGES_CATALOG_PATH, "uploaded.json")
    if os.path.exists(uploaded_json_path):
        with open(uploaded_json_path, "r") as f:
            try:
                uploaded_data = json.load(f)
                if not isinstance(uploaded_data, list):
                    uploaded_data = []
            except json.JSONDecodeError:
                uploaded_data = []
    else:
        uploaded_data = []

    uploaded_set = set(uploaded_data)

    # Get all images in IMAGES_CATALOG_PATH
    images = glob.glob(os.path.join(IMAGES_CATALOG_PATH, "*"))
    images = [img for img in images if os.path.isfile(img) and not img.endswith(".json")]

    # Filter out already uploaded images and limit to FILES_LIMIT
    not_uploaded_images = [img for img in images if os.path.basename(img) not in uploaded_set]
    to_upload = not_uploaded_images[:FILES_LIMIT]

    # Limit concurrency
    semaphore = asyncio.Semaphore(8)

    tasks = []
    for image_path in to_upload:
        task = asyncio.create_task(process_image(image_path, uploaded_set, semaphore, uploaded_json_path))
        tasks.append(task)

    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful_uploads = sum(1 for res in results if res is True)
    else:
        successful_uploads = 0

    print(f"[INFO] Done. Successfully uploaded {successful_uploads} images.")


if __name__ == "__main__":
    asyncio.run(main())
