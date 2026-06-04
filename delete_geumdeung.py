import os
import shutil

# Target directories and files to delete
targets = [
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Geumdeungjisa",
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\scripts\download_geumdeung_images.py",
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\scripts\generate_tts_geumdeung.py",
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\scripts\render_shorts_geumdeung.py",
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Empress_Longform",
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\scripts\render_empress_video.py"
]

print("Starting deletion of Geumdeungjisa related contents...")

for target in targets:
    if os.path.exists(target):
        try:
            if os.path.isdir(target):
                shutil.rmtree(target)
                print(f"Deleted directory: {target}")
            else:
                os.remove(target)
                print(f"Deleted file: {target}")
        except Exception as e:
            print(f"Error deleting {target}: {e}")
    else:
        print(f"Target not found: {target}")

print("Deletion process completed!")
