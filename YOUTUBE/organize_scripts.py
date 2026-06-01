import os
import shutil

base_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE"
scripts_dir = os.path.join(base_dir, "scripts")
os.makedirs(scripts_dir, exist_ok=True)

files_to_move = [
    "cleanup_youtube.py",
    "create_outro_anim.py",
    "generate_no_subs_script.py",
    "generate_tts.py",
    "generate_tts_fix.py",
    "generate_tts_subway.py",
    "mix_all_audio.py",
    "mix_audio.py",
    "render_empress_video.py",
    "render_no_subs.py",
    "render_shorts.py",
    "render_video.py",
    "render_video_30cuts.py"
]

print("Moving files to YOUTUBE/scripts:")
for file in files_to_move:
    src_path = os.path.join(base_dir, file)
    dest_path = os.path.join(scripts_dir, file)
    if os.path.exists(src_path):
        # Move the file (overwrite if exists)
        if os.path.exists(dest_path):
            os.remove(dest_path)
        shutil.move(src_path, dest_path)
        print(f"Moved: {file}")
    else:
        print(f"File not found, skipped: {file}")

# Delete old check_and_copy.py and render_shorts_subway.py from root
old_root_files = ["check_and_copy.py", "render_shorts_subway.py"]
for file in old_root_files:
    old_path = os.path.join(base_dir, file)
    if os.path.exists(old_path):
        os.remove(old_path)
        print(f"Deleted old root file: {file}")

print("\nReorganization complete! You can now delete this organize_scripts.py file.")
