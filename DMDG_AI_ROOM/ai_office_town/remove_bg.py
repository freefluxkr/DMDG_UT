import os
from rembg import remove
from PIL import Image

dots_dir = r"C:\Users\tuesv\Documents\DMDG_UT\DMDG_AI_ROOM\ai_office_town\assets\images\dots"
out_dir = r"C:\Users\tuesv\Documents\DMDG_UT\DMDG_AI_ROOM\ai_office_town\assets\images"

import glob
jpeg_files = glob.glob(os.path.join(dots_dir, "*.jpeg"))

for input_path in jpeg_files:
    base_name = os.path.basename(input_path)
    name_only = os.path.splitext(base_name)[0]
    out_filename = name_only + ".png"
    output_path = os.path.join(out_dir, out_filename)
    
    print(f"Processing {base_name}...")
    try:
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        print(f"Success: saved to {out_filename}")
    except Exception as e:
        print(f"Error processing {base_name}: {e}")

print("Background removal for dots complete.")
