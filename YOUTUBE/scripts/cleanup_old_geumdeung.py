import os
import shutil

TARGET_DIRS = [
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Geumdeungjisa\assets_image",
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Geumdeungjisa\exports",
    r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Geumdeungjisa\assets_video"
]

ssamples_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\ssamples"

print("=== STARTING CLEANUP AND REMOVAL ===")

# Clear contents of the 3 main directories
for dir_path in TARGET_DIRS:
    if os.path.exists(dir_path):
        print(f"\nCleaning directory contents: {dir_path}")
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if item == ".gitkeep":
                continue
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    print(f"  Deleted file: {item}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"  Deleted directory: {item}")
            except Exception as e:
                print(f"  Error deleting {item}: {e}")
    else:
        print(f"\nDirectory not found: {dir_path}")

# Delete the ssamples directory completely
if os.path.exists(ssamples_dir):
    print(f"\nDeleting ssamples directory completely: {ssamples_dir}")
    try:
        shutil.rmtree(ssamples_dir)
        print("  Deleted ssamples folder successfully.")
    except Exception as e:
        print(f"  Error deleting ssamples folder: {e}")
else:
    print(f"\nssamples directory already deleted: {ssamples_dir}")

print("\n=== CLEANUP COMPLETED SUCCESSFULLY ===")
