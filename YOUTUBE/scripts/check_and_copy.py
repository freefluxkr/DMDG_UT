import os
import shutil
import subprocess

src_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\9d3e92a0-7e67-43f2-9ee3-bd04473881bf"
dest_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\assets_image"
exports_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\exports"

os.makedirs(dest_dir, exist_ok=True)
os.makedirs(exports_dir, exist_ok=True)

# 1. Clean up/delete all real photo files containing foreigners or real photo styles to avoid usage
photos_to_delete = [
    "subway_escalator_hook.png",
    "subway_priority_seat.png",
    "subway_priority_seat_1.png",
    "subway_priority_seat_2.png",
    "subway_screen_door.png",
    "subway_screen_door_1.png",
    "subway_screen_door_2.png",
    "subway_transfer_bump.png",
    "subway_stairs_line.png"
]

print("Cleaning up old photo files:")
for photo in photos_to_delete:
    photo_path = os.path.join(dest_dir, photo)
    if os.path.exists(photo_path):
        os.remove(photo_path)
        print(f"Deleted old photo: {photo}")

# 2. Copy only the newly generated Sumukhwa images
files_to_copy = {
    "subway_escalator_1_1780293381171.png": "subway_escalator_1.png",
    "subway_escalator_2_1780293403132.png": "subway_escalator_2.png",
    "subway_bump_1_1780308274283.png": "subway_bump_1.png",
    "subway_bump_2_1780308297409.png": "subway_bump_2.png",
    "subway_stairs_1_1780309110630.png": "subway_stairs_1.png",
    "subway_stairs_2_1780309130291.png": "subway_stairs_2.png",
    "subway_priority_seat_1_1780308478764.png": "subway_priority_seat_1.png",
    "subway_priority_seat_2_1780308496120.png": "subway_priority_seat_2.png",
    "subway_screen_door_1_1780308513586.png": "subway_screen_door_1.png",
    "subway_screen_door_2_1780308532366.png": "subway_screen_door_2.png"
}

print("\nCopying sumukhwa files from brain:")
for src_name, dest_name in files_to_copy.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"Copied {src_name} to {dest_name}")
    else:
        print(f"Source not found: {src_path}")

print("\nFiles remaining in assets_image:")
print(os.listdir(dest_dir))

print("\nRunning rendering script:")
script_path = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\scripts\render_shorts_subway.py"
res = subprocess.run(["python", script_path], capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
print("STDERR:")
print(res.stderr)

print("\nFiles in exports:")
if os.path.exists(exports_dir):
    print(os.listdir(exports_dir))
else:
    print("Exports directory does not exist")
