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
                # Decrease dimensions step by step, but not below MIN_SIDE
                if current_width > MIN_SIDE:
                    current_width -= SIZE_STEP
                if current_height > MIN_SIDE:
                    current_height -= SIZE_STEP

                if current_width < MIN_SIDE:
                    current_width = MIN_SIDE
                if current_height < MIN_SIDE:
                    current_height = MIN_SIDE

                # Resize image with LANCZOS filter
                resized_img = img.resize((current_width, current_height), Image.Resampling.LANCZOS)

                # Save to a temp file to check size
                temp_path = img_path + ".temp"
                resized_img.save(temp_path, "webp", quality=quality, method=6)

                new_size = os.path.getsize(temp_path)

                if new_size <= MAX_FILE_SIZE or current_width <= MIN_SIDE or current_height <= MIN_SIDE or quality <= 10:
                    if new_size <= MAX_FILE_SIZE:
                        # Overwrite original
                        os.replace(temp_path, img_path)
                        print(f"[INFO] {os.path.basename(img_path)} reduced to {new_size} bytes.")
                    else:
                        # Couldn't reduce below conditions
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
    except Exception as e:
        print(f"[ERROR] Could not process {os.path.basename(img_path)}: {e}")


def main():
    # Get all webp images
    images = glob.glob(os.path.join(IMAGES_DIR, "*.webp"))

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(process_image, img) for img in images]
        for f in as_completed(futures):
            exc = f.exception()
            if exc:
                print(f"[ERROR] Exception occurred: {exc}")

    print("[INFO] Done processing images.")


if __name__ == "__main__":
    main()
