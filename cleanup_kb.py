import os
import shutil

project_dir = r"c:\Users\user\Documents\DMDG_UT"
old_kb = os.path.join(project_dir, ".agent", "knowledge_base")
new_kb = os.path.join(project_dir, "AI_Knowledge_Base")
new_meetings = os.path.join(new_kb, "meetings")

print("--- Merging Knowledge Bases ---")
if os.path.exists(old_kb):
    for item in os.listdir(old_kb):
        src = os.path.join(old_kb, item)
        dst = os.path.join(new_meetings, item)
        
        # Skip directories like .obsidian or existing junctions
        if item in [".obsidian", "대화록", "회의록"]:
            continue
            
        if os.path.exists(src):
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.move(src, dst)
                print(f"Moved directory: {item} -> AI_Knowledge_Base/meetings/")
            else:
                shutil.move(src, dst)
                print(f"Moved file: {item} -> AI_Knowledge_Base/meetings/")
                
    # Remove old knowledge_base folder (handling junctions we made inside it first)
    old_daehwa = os.path.join(old_kb, "대화록")
    old_hoeui = os.path.join(old_kb, "회의록")
    
    # In Windows, junctions should be removed using rmdir or os.unlink
    # in python os.unlink or os.rmdir works for junctions
    for link_path in [old_daehwa, old_hoeui]:
        if os.path.exists(link_path):
            try:
                os.rmdir(link_path)
                print(f"Removed old junction: {os.path.basename(link_path)}")
            except Exception as e:
                print(f"Failed to remove junction {link_path}: {e}")
                
    try:
        shutil.rmtree(old_kb)
        print("Successfully removed old redundant .agent/knowledge_base folder!")
    except Exception as e:
        print(f"Could not remove old folder: {e}")
else:
    print("Old knowledge base not found or already merged.")

# Clean up temp test files in root
temp_files = ["test_link.py", "test_powershell.py", "link_obsidian.py", "cross_link.py"]
print("\n--- Cleaning up temporary scripts ---")
for f in temp_files:
    p = os.path.join(project_dir, f)
    if os.path.exists(p):
        os.remove(p)
        print(f"Removed temporary file: {f}")

print("\nCleanup completed!")
