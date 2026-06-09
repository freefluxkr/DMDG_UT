import os
import shutil

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
US_DIR = os.path.join(BASE_DIR, r"YOUTUBE\Projects\TempleFoodUS")
SRC_DIR = os.path.join(US_DIR, "assets_image_new")
DEST_DIR = os.path.join(US_DIR, "assets_image")

os.makedirs(DEST_DIR, exist_ok=True)

# Define mapping based on prefixes (e.g., scene1, scene2, ...)
MAPPING = {
    "scene1": "scene1.png",
    "scene2": "scene2.png",
    "scene3": "scene3.png",
    "scene4": "scene4.png",
    "scene5": "scene5.png",
    "scene6": "scene6.png",
    "scene7": "scene7.png",
    "scene8": "scene8.png"
}

files = os.listdir(SRC_DIR)
for f in files:
    for prefix, dest_name in MAPPING.items():
        if f.startswith(prefix):
            src_path = os.path.join(SRC_DIR, f)
            dest_path = os.path.join(DEST_DIR, dest_name)
            shutil.copy2(src_path, dest_path)
            print(f"Copied and renamed: {f} -> {dest_name}")
            break
