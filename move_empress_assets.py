import os
import shutil

base_dir = r"c:\Users\user\Documents\DMDG_UT"

old_audio_dir = os.path.join(base_dir, r"YOUTUBE\result\audio\longform")
new_audio_dir = os.path.join(base_dir, r"YOUTUBE\Projects\Empress_Longform\assets_audio")

# 폴더가 없으면 무조건 생성합니다!
os.makedirs(new_audio_dir, exist_ok=True)

# Move all MP3 files
moved_count = 0
if os.path.exists(old_audio_dir):
    for filename in os.listdir(old_audio_dir):
        if filename.endswith(".mp3"):
            src = os.path.join(old_audio_dir, filename)
            dst = os.path.join(new_audio_dir, filename)
            shutil.move(src, dst)
            moved_count += 1

print(f"Moved {moved_count} Empress audio files to new project folder.")
