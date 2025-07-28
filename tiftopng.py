import os
from PIL import Image

# Set your root folder here
ROOT_DIR = r"C:/Users/xxx"

# Delete .tif after conversion?
DELETE_TIF = False

def convert_tif_to_png():
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.lower().endswith(".tif"):
                tif_path = os.path.join(root, file)
                png_path = os.path.splitext(tif_path)[0] + ".png"

                if os.path.exists(png_path):
                    print(f"Skipped (already exists): {png_path}")
                    continue

                try:
                    print(f"Converting: {tif_path}")
                    img = Image.open(tif_path)
                    img.save(png_path, "PNG")

                    if DELETE_TIF:
                        os.remove(tif_path)
                        print(f"Deleted original: {tif_path}")

                except Exception as e:
                    print(f"Failed: {tif_path} — {e}")

convert_tif_to_png()
