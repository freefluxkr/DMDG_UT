import os
import shutil

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE"
NOTES_DIR = r"c:\Users\user\Documents\DMDG_UT\회의록"

# 1. Move important markdown files to 회의록
impl_dir = os.path.join(BASE_DIR, "impl")
if os.path.exists(impl_dir):
    proposal_file = os.path.join(impl_dir, "viral_content_proposal.md")
    if os.path.exists(proposal_file):
        shutil.move(proposal_file, os.path.join(NOTES_DIR, "viral_content_proposal.md"))
        print("Moved viral_content_proposal.md to 회의록")
    shutil.rmtree(impl_dir)
    print("Deleted impl folder")

# 2. Delete empty docs folder
docs_dir = os.path.join(BASE_DIR, "docs")
if os.path.exists(docs_dir):
    shutil.rmtree(docs_dir)
    print("Deleted docs folder")

# 3. Delete dummy / test files
files_to_delete = [
    "test.txt",
    "test_scroll.mp4",
    "create_dummy_sfx.py",
    "download_real_sfx.py"
]

for f in files_to_delete:
    filepath = os.path.join(BASE_DIR, f)
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Deleted {f}")

print("Cleanup complete!")
