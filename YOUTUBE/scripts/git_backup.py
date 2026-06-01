import subprocess
import os

cwd = r"c:\Users\user\Documents\DMDG_UT"
os.chdir(cwd)

print("Demis executing git add...")
subprocess.run(["git", "add", "."])

print("Demis executing git commit...")
subprocess.run(["git", "commit", "-m", "feat: finalize Subway Shorts & Geumdeungjisa scenario layout"])

print("Demis executing git push...")
subprocess.run(["git", "push"])

print("Git backup completed successfully!")
