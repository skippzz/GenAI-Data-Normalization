import os
from PIL import Image

# Root to scan
ROOT_DIR = r"C:\Users\xxx"
TARGET_SIZE = (1024, 1024)
TARGET_KEYWORD = "xxx"
VALID_EXTENSIONS = (".tif", ".tiff")

# Supported fallback mode
FALLBACK_MODE = "RGB"

for dirpath, _, filenames in os.walk(ROOT_DIR):
    for file in filenames:
        if TARGET_KEYWORD.lower() not in file.lower():
            continue
        if not file.lower().endswith(VALID_EXTENSIONS):
            continue

        full_path = os.path.join(dirpath, file)

        try:
            with Image.open(full_path) as img:
                width, height = img.size

                # Convert to a safe mode (RGB)
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert(FALLBACK_MODE)

                if width > 1024 or height > 1024:
                    img = img.resize(TARGET_SIZE, Image.LANCZOS)

                    # Overwrite original
                    img.save(full_path)
                    print(f"Resized: {full_path}")
                else:
                    print(f"Skipped (already small): {full_path}")

        except Exception as e:
            print(f"Error processing {full_path}: {e}")
