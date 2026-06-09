import subprocess
import os

cwd = r"c:\Users\user\Documents\DMDG_UT"
os.chdir(cwd)

print("Executing git status...")
subprocess.run(["git", "status"])

print("\nExecuting git add...")
subprocess.run(["git", "add", "."])

commit_message = "feat: add 16:9 widescreen US temple food scripts, guest outline, and corrected characters description"
print(f"\nExecuting git commit -m '{commit_message}'...")
subprocess.run(["git", "commit", "-m", commit_message])

print("\nExecuting git push...")
subprocess.run(["git", "push"])

print("\nGit commit & push completed successfully!")
