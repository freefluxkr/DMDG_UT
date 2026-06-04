import os
import shutil

src_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\c6683569-69ce-4e06-9853-2a29ec207822"
dest_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Geumdeungjisa\assets_image"

mapping = {
    "geumdeung_box_1780360502692.png": "geumdeung_shorts_box.png",
    "geumdeung_sad_1780360486412.png": "geumdeung_shorts_sad.png",
    "geumdeung_write_1780360522739.png": "geumdeung_shorts_write.png",
    "geumdeung_jeongjo_1780360466705.png": "geumdeung_shorts_jeongjo.png"
}

os.makedirs(dest_dir, exist_ok=True)

for src_name, dest_name in mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"Copied {src_name} to {dest_name}")
    else:
        print(f"Source not found: {src_path}")

print("Image copy process completed!")
