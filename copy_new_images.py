import os
import shutil

src_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\c6683569-69ce-4e06-9853-2a29ec207822"
dest_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Geumdeungjisa\assets_image"

os.makedirs(dest_dir, exist_ok=True)

mapping = {
    "shorts_box_1780369930049.png": "geumdeung_shorts_box.png",
    "shorts_sad_1780369957723.png": "geumdeung_shorts_sad.png",
    "shorts_write_1780369982346.png": "geumdeung_shorts_write.png",
    "shorts_jeongjo_1780370002994.png": "geumdeung_shorts_jeongjo.png"
}

print("=== COPYING GENERATED VERTICAL 9:16 IMAGES ===")
for src_name, dest_name in mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if os.path.exists(src_path):
        try:
            shutil.copy(src_path, dest_path)
            print(f"Successfully copied: {src_name} -> {dest_name}")
        except Exception as e:
            print(f"Error copying {src_name}: {e}")
    else:
        print(f"Source file not found: {src_path}")

print("=== IMAGE COPY COMPLETED ===")
