import os
import shutil

base_dir = r"c:\Users\user\Documents\DMDG_UT"

dirs_to_create = [
    r"AI_Knowledge_Base\meetings",
    r"AI_Knowledge_Base\guidelines",
    r"AI_Knowledge_Base\instructions",
    r"YOUTUBE\Projects\Empress_Longform\scripts",
    r"YOUTUBE\Projects\Empress_Longform\assets_audio",
    r"YOUTUBE\Projects\Empress_Longform\assets_image",
    r"YOUTUBE\Projects\Empress_Longform\exports",
    r"YOUTUBE\Projects\Subway_Shorts\scripts",
    r"YOUTUBE\Projects\Subway_Shorts\assets_audio",
    r"YOUTUBE\Projects\Subway_Shorts\assets_image",
    r"YOUTUBE\Projects\Subway_Shorts\exports"
]

for d in dirs_to_create:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files_to_move = [
    (r"회의록\008_shorts_script_subway_manners.md", r"YOUTUBE\Projects\Subway_Shorts\scripts\008_shorts_script_subway_manners.md"),
    (r"YOUTUBE\narration\long\001_dmdg_free_empress_longform.md", r"YOUTUBE\Projects\Empress_Longform\scripts\001_dmdg_free_empress_longform.md")
]

for src, dst in files_to_move:
    src_path = os.path.join(base_dir, src)
    dst_path = os.path.join(base_dir, dst)
    if os.path.exists(src_path):
        shutil.move(src_path, dst_path)

print("Folders created and files moved successfully.")
