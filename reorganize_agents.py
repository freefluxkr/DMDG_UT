import os
import shutil

agent_dir = r".agent"

# 1. assets renaming
assets_rename = {
    "leo_profile.png": "demis_profile.png",
    "luna_greeting_pixar.png": "jennifer_profile.png",
    "김작가.png": "haruki_profile.png",
    "영숙에이전트비서.jpeg": "peggy_profile.jpeg",
    "정팀장.png": "upd_profile.png",
    "조박사.png": "mustafa_profile.png",
    "코다리.png": "craig_profile.png",
    "탐정박.png": "sherlock_profile.png",
    "현빈.jpeg": "satya_profile.jpeg"
}

print("--- Assets Reorganization ---")
assets_path = os.path.join(agent_dir, "assets")
for old, new in assets_rename.items():
    old_file = os.path.join(assets_path, old)
    new_file = os.path.join(assets_path, new)
    if os.path.exists(old_file):
        shutil.move(old_file, new_file)
        print(f"Moved: {old} -> {new}")
    else:
        print(f"Skipped (Not Found): {old}")

# 2. portraits renaming
portraits_rename = {
    "drjo.png": "mustafa.png",
    "hyunsoo.png": "zimmer.png",
    "kodari.png": "craig.png",
    "leo.png": "demis.png",
    "luna.png": "jennifer.png",
    "minjun.png": "satya.png",
    "writer_kim.png": "haruki.png",
    "youngsook.png": "peggy.png"
}

print("\n--- Portraits Reorganization ---")
portraits_path = os.path.join(agent_dir, "portraits")
for old, new in portraits_rename.items():
    old_file = os.path.join(portraits_path, old)
    new_file = os.path.join(portraits_path, new)
    if os.path.exists(old_file):
        shutil.move(old_file, new_file)
        print(f"Moved: {old} -> {new}")
    else:
        print(f"Skipped (Not Found): {old}")

# Add sherlock portrait
sherlock_portrait = os.path.join(portraits_path, "sherlock.png")
sherlock_asset = os.path.join(assets_path, "sherlock_profile.png")
if os.path.exists(sherlock_asset) and not os.path.exists(sherlock_portrait):
    shutil.copy(sherlock_asset, sherlock_portrait)
    print(f"Copied portrait for Sherlock from {sherlock_asset}")

# 3. skills renaming
skills_rename = {
    "ceo": "demis",
    "secretary": "peggy",
    "analyst": "mustafa",
    "designer": "jennifer",
    "kodari": "craig",
    "scriptwriter": "haruki",
    "sound_director": "zimmer",
    "searcher": "sherlock",
    "video": "upd"
}

print("\n--- Skills Reorganization ---")
skills_path = os.path.join(agent_dir, "skills")
for old, new in skills_rename.items():
    old_folder = os.path.join(skills_path, old)
    new_folder = os.path.join(skills_path, new)
    if os.path.exists(old_folder):
        if os.path.exists(new_folder):
            shutil.rmtree(new_folder)
        shutil.move(old_folder, new_folder)
        print(f"Moved folder: {old} -> {new}")
    else:
        print(f"Skipped folder (Not Found): {old}")

# Remove old deprecated skills/sound
sound_skill_path = os.path.join(skills_path, "sound")
if os.path.exists(sound_skill_path):
    shutil.rmtree(sound_skill_path)
    print("Removed deprecated skills/sound folder")

# 4. inbox directories
print("\n--- Inbox Reorganization ---")
inbox_path = os.path.join(agent_dir, "inbox")
target_inboxes = ["demis", "peggy", "mustafa", "jennifer", "craig", "haruki", "zimmer", "satya", "sherlock", "upd", "all"]
for target in target_inboxes:
    p = os.path.join(inbox_path, target)
    if not os.path.exists(p):
        os.makedirs(p)
        print(f"Created inbox folder: {target}")

print("\nReorganization script completed successfully!")
