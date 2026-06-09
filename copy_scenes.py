import shutil
import os

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
TARGET_DIR = os.path.join(BASE_DIR, r"YOUTUBE\Projects\TempleFoodUS\assets_image")
os.makedirs(TARGET_DIR, exist_ok=True)

MAPPING = {
    "scene1.png": r"C:\Users\user\.gemini\antigravity-ide\brain\5b2c16cb-f324-41a5-a61b-fd76a65d8e30\scene1_1780971547277.png",
    "scene2.png": r"C:\Users\user\.gemini\antigravity-ide\brain\5b2c16cb-f324-41a5-a61b-fd76a65d8e30\scene2_1780971563298.png",
    "scene3.png": r"C:\Users\user\.gemini\antigravity-ide\brain\5b2c16cb-f324-41a5-a61b-fd76a65d8e30\scene3_1780971583149.png",
    "scene4.png": r"C:\Users\user\.gemini\antigravity-ide\brain\5b2c16cb-f324-41a5-a61b-fd76a65d8e30\scene4_1780971599342.png",
    "scene5.png": r"C:\Users\user\.gemini\antigravity-ide\brain\5b2c16cb-f324-41a5-a61b-fd76a65d8e30\scene5_1780971614465.png",
    "scene6.png": r"C:\Users\user\.gemini\antigravity-ide\brain\5b2c16cb-f324-41a5-a61b-fd76a65d8e30\scene6_1780971631983.png",
    "scene7.png": r"C:\Users\user\.gemini\antigravity-ide\brain\5b2c16cb-f324-41a5-a61b-fd76a65d8e30\scene7_1780971665238.png",
    "scene8.png": r"C:\Users\user\.gemini\antigravity-ide\brain\5b2c16cb-f324-41a5-a61b-fd76a65d8e30\scene8_1780971697281.png"
}

for name, path in MAPPING.items():
    if os.path.exists(path):
        dest = os.path.join(TARGET_DIR, name)
        shutil.copy2(path, dest)
        print(f"Copied {name} to {dest}")
    else:
        print(f"Error: {path} does not exist.")
