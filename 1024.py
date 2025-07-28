from PIL import Image, ImageFile # Import ImageFile
import os

# Allow Pillow to load truncated images.
# Use this with caution, as it means you might be processing incomplete files.
ImageFile.LOAD_TRUNCATED_IMAGES = True

def resize_images_in_directory(root_dir, target_size=(1024, 1024)):
    """
    Resizes PNG and TIFF images in a given directory and all its subdirectories
    to the target_size (default 1024x1024).

    Args:
        root_dir (str): The starting directory to search for images.
        target_size (tuple): A tuple (width, height) for the desired image size.
    """
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            file_name_without_ext, ext = os.path.splitext(file)
            ext = ext.lower()

            if ext in ['.png', '.tif', '.tiff']:
                try:
                    with Image.open(file_path) as img:
                        # Convert to RGBA to handle potential transparency in PNGs and ensure compatibility
                        # for various image types like normals, roughness etc.
                        img = img.convert("RGBA")

                        # Resize the image
                        img_resized = img.resize(target_size, Image.LANCZOS) # LANCZOS is a high-quality downsampling filter

                        # Save the resized image, overwriting the original
                        # For TIFF, ensure proper saving based on original mode if possible,
                        # but RGBA is a good general choice.
                        if ext == '.png':
                            img_resized.save(file_path, optimize=True)
                        elif ext in ['.tif', '.tiff']:
                            # TIFF can have various internal structures; saving as PNG or a new TIFF
                            # might be more reliable if original structure is complex.
                            # For simplicity and general compatibility, saving as TIFF with compression.
                            # If issues arise, consider saving as PNG in a new directory or
                            # investigating specific TIFF saving options for your use case.
                            img_resized.save(file_path, compression="tiff_lzw")

                        print(f"Resized and saved: {file_path}")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            else:
                print(f"Skipping non-image file: {file_path}")

if __name__ == "__main__":
    # This is the best option for Windows file paths in Python.
    root_directory = r'C:\Users\xxx'

    if not os.path.isdir(root_directory):
        print(f"Error: The directory '{root_directory}' does not exist.")
        print("Please ensure the path is correct and the directory exists.")
    else:
        print(f"Starting image resizing process in: {root_directory}")
        resize_images_in_directory(root_directory)
        print("\nImage resizing process completed.")
        print("Please review the processed images. Some specialized TIFF formats might not save perfectly.")