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

FILES_LIMIT = 100

# Note: All logging and comments in English
# This script uploads images to Backblaze and Qdrant asynchronously.
# Steps per image:
# 1. Check if image was already uploaded (by checking uploaded.json).
# 2. If not uploaded, upload to Backblaze.
# 3. Vectorize image.
# 4. Upload vector to Qdrant.
# 5. Mark as uploaded in uploaded.json.
#
# We use an asyncio Semaphore to limit concurrency to 8 parallel tasks.
# We stop after FILES_LIMIT images are successfully uploaded.

backblaze = Backblaze()
qdrant = QdrantService()
qdrant.create_collection_if_not_exists()


async def process_image(image_path: str, uploaded_set: set, semaphore: asyncio.Semaphore, uploaded_images: List[str]) -> bool:
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

        # 4. Mark as uploaded
        uploaded_images.append(image_name)
        print(f"[INFO] {image_name} marked as uploaded.")
        return True


async def main():
    # Load or create uploaded.json
    uploaded_json_path = os.path.join(IMAGES_CATALOG_PATH, "uploaded.json")
    if os.path.exists(uploaded_json_path):
        with open(uploaded_json_path, "r") as f:
            try:
                uploaded_data = json.load(f)
            except json.JSONDecodeError:
                uploaded_data = []
    else:
        uploaded_data = []

    uploaded_set = set(uploaded_data)

    # Get all images in IMAGES_CATALOG_PATH
    # Adjust this pattern if needed (assuming all images end with .jpg/.png)
    images = glob.glob(os.path.join(IMAGES_CATALOG_PATH, "*"))
    images = [img for img in images if os.path.isfile(img) and not img.endswith(".json")]

    # Limit concurrency
    semaphore = asyncio.Semaphore(8)

    # We'll process images until we hit FILES_LIMIT successful uploads
    uploaded_images = []
    tasks = []
    successful_uploads = 0

    for image_path in images:
        if successful_uploads >= FILES_LIMIT:
            print("[INFO] Daily FILES_LIMIT reached, stopping.")
            break
        image_name = os.path.basename(image_path)
        if image_name not in uploaded_set:
            task = asyncio.create_task(process_image(image_path, uploaded_set, semaphore, uploaded_images))
            tasks.append(task)

    # Run tasks and wait for them to complete
    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Count how many were successful
        for res in results:
            if res is True:
                successful_uploads += 1
                if successful_uploads >= FILES_LIMIT:
                    print("[INFO] FILES_LIMIT reached during processing. Stopping further tasks.")
                    break

    # Update uploaded.json with newly uploaded images
    if uploaded_images:
        with open(uploaded_json_path, "r") as f:
            try:
                current_data = json.load(f)
                if not isinstance(current_data, list):
                    current_data = []
            except json.JSONDecodeError:
                current_data = []
        current_set = set(current_data)
        current_set.update(uploaded_images)
        with open(uploaded_json_path, "w") as f:
            json.dump(list(current_set), f, indent=2)
        print("[INFO] uploaded.json updated.")

    print(f"[INFO] Done. Successfully uploaded {successful_uploads} images.")


if __name__ == "__main__":
    asyncio.run(main())
