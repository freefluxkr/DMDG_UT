import os
import shutil

agent_dir = r".agent"
assets_path = os.path.join(agent_dir, "assets")
portraits_path = os.path.join(agent_dir, "portraits")

# Copy upd portrait
upd_portrait = os.path.join(portraits_path, "upd.png")
upd_asset = os.path.join(assets_path, "upd_profile.png")
if os.path.exists(upd_asset):
    shutil.copy(upd_asset, upd_portrait)
    print("Copied portrait for UPD to portraits/upd.png")

print("Portrait copy fixed!")
