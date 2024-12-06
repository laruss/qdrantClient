import os
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

# Configuration
IMAGES_DIR = "path/to/images"
MAX_FILE_SIZE = 1_000_000  # 1MB
QUALITY_STEP = 10
SIZE_STEP = 100
MIN_SIDE = 1024
CONCURRENCY = 8

# Note: This script will iterate through all webp files in a directory.
# For each file > 1MB, it will iteratively reduce quality and dimensions
# until the file size is below 1MB or one of the image sides is less than 1024px.
#
# Steps:
# 1. Check if the image file is > 1MB.
#    - If no, skip.
# 2. If yes, open the image and start iterative reduction:
#    - Decrease dimensions by SIZE_STEP px and quality by QUALITY_STEP each iteration.
#    - Save in memory and check the size by temporarily writing to disk or using BytesIO.
#    - Repeat until conditions are met or impossible to reduce further.
#
# Dimensions reduction strategy:
# - Reduce width and height by SIZE_STEP each iteration (but never below MIN_SIDE)
# Quality reduction strategy:
# - Start from 100 and go down by QUALITY_STEP each iteration until 10 (minimum reasonable quality).
#
# Once done, overwrite the original file if the size condition is met.

def process_image(img_path: str):
    # Check initial file size
    initial_size = os.path.getsize(img_path)
    if initial_size <= MAX_FILE_SIZE:
        # Image is already below threshold, skip
        print(f"[INFO] {os.path.basename(img_path)} is already <1MB, skipping.")
        return

    # Open image
    try:
        with Image.open(img_path) as img:
            img = img.convert("RGB")  # ensure RGB for webp saving
            width, height = img.size

            # Initial settings
            quality = 100
            current_width, current_height = width, height

            while True:
                # Ensure we don't go below MIN_SIDE
                if current_width > MIN_SIDE:
                    current_width -= SIZE_STEP
                if current_height > MIN_SIDE:
                    current_height -= SIZE_STEP

                # Ensure dimensions don't go below MIN_SIDE
                if current_width < MIN_SIDE:
                    current_width = MIN_SIDE
                if current_height < MIN_SIDE:
                    current_height = MIN_SIDE

                # Resize image
                resized_img = img.resize((current_width, current_height), Image.ANTIALIAS)

                # Save to a temp file (or in-memory) to check size
                temp_path = img_path + ".temp"
                resized_img.save(temp_path, "webp", quality=quality, method=6)

                new_size = os.path.getsize(temp_path)

                if new_size <= MAX_FILE_SIZE or current_width <= MIN_SIDE or current_height <= MIN_SIDE or quality <= 10:
                    # If conditions met or can't reduce further, break
                    if new_size <= MAX_FILE_SIZE:
                        # Overwrite original
                        os.replace(temp_path, img_path)
                        print(f"[INFO] {os.path.basename(img_path)} reduced to {new_size} bytes.")
                    else:
                        # Couldn't reduce below 1MB before hitting dimension/quality limit,
                        # so remove temp file
                        os.remove(temp_path)
                        print(f"[WARN] {os.path.basename(img_path)} could not be reduced under conditions.")
                    break
                else:
                    # Remove temp and continue iteration
                    os.remove(temp_path)
                    # Reduce quality further
                    quality -= QUALITY_STEP
                    if quality < 10:
                        quality = 10
                        # On next iteration if still not good, we'll break out.
    except Exception as e:
        print(f"[ERROR] Could not process {os.path.basename(img_path)}: {e}")


def main():
    # Get all webp images
    images = glob.glob(os.path.join(IMAGES_DIR, "*.webp"))

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(process_image, img) for img in images]
        for f in as_completed(futures):
            # We don't need the result specifically,
            # but we handle exceptions if any
            exc = f.exception()
            if exc:
                print(f"[ERROR] Exception occurred: {exc}")

    print("[INFO] Done processing images.")


if __name__ == "__main__":
    main()
