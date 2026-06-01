import os
import urllib.request
import urllib.parse
import time

dest_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\assets_image"
os.makedirs(dest_dir, exist_ok=True)

prompts = {
    "subway_bump_1.png": "A crowded Korean subway station transfer passage during bright broad daylight, busy commuters in modern clothes walking fast, motion blur, realistic, high detail, cinematic, depth of field, 9:16 aspect ratio, no text.",
    "subway_bump_2.png": "First-person perspective walking through a packed Korean subway terminal in bright daytime, people rushing past closely, motion blur, realistic photograph, cinematic lighting, 9:16 aspect ratio, no text."
}

print("Downloading new daylight bump images from Pollinations:")
for filename, prompt in prompts.items():
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&seed=4567"
    dest_path = os.path.join(dest_dir, filename)
    
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            with open(dest_path, "wb") as f:
                f.write(response.read())
        print(f"Successfully saved to {dest_path}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
    time.sleep(1)
