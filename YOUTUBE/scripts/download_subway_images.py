import os
import urllib.request
import urllib.parse
import time

dest_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\assets_image"
os.makedirs(dest_dir, exist_ok=True)

# Lower resolution (512x912) is still 9:16 but bypasses the high-res premium rate limits (HTTP 402)
prompts = {
    "subway_bump_1.png": {
        "prompt": "A crowded Korean subway transfer station in broad bright daylight, busy commuters in modern clothes rushing, a dramatic close-up of a rude shoulder-bumping moment between two people, modern Korean ink wash painting style, sumukhwa, high contrast, sharp brush strokes, no text",
        "seed": 1001
    },
    "subway_bump_2.png": {
        "prompt": "First-person perspective of a crowded Korean subway terminal in bright daytime, people rushing past closely causing friction, modern Korean ink wash painting style, sumukhwa, high contrast, no text",
        "seed": 1002
    },
    "subway_stairs_1.png": {
        "prompt": "A long, steep subway station staircase crowded with a massive line-cutting rush of people like a school of salmon, captured in a high-vertical wide angle view suitable for a downward panning shot, modern Korean ink wash painting style, sumukhwa, no text",
        "seed": 2001
    },
    "subway_stairs_2.png": {
        "prompt": "Looking down a packed subway staircase with people rushing and pushing past each other in a hurry, vertical layout, modern Korean ink wash painting style, sumukhwa, no text",
        "seed": 2002
    },
    "subway_priority_seat_1.png": {
        "prompt": "A young passenger wearing noise-canceling headphones sitting on a subway priority seat looking down at a smartphone, ignoring an elderly passenger standing right in front of them, modern Korean ink wash painting style, sumukhwa, no text",
        "seed": 3001
    },
    "subway_priority_seat_2.png": {
        "prompt": "A close-up of a young person sitting comfortably on a Korean subway priority seat (경로석) with headphones on, a senior citizen standing in front of them, modern Korean ink wash painting style, sumukhwa, no text",
        "seed": 3002
    },
    "subway_screen_door_1.png": {
        "prompt": "A closing glass screen door at a subway station platform. Reflected on the dark metallic glass surface are faint, eerie silhouettes of people smiling and laughing with shameless, empty eyes, holding smartphones. Behind the glass, a dark train is departing. Modern Korean ink wash painting style, sumukhwa, dark and contrasting tones, cynical mood, high detail, no text",
        "seed": 4001
    },
    "subway_screen_door_2.png": {
        "prompt": "The glass subway screen door closed shut, reflecting creepy and shameless smiling silhouettes of commuters staring into their phones, modern Korean ink wash painting style, sumukhwa, dark and cold tones, high detail, no text",
        "seed": 4002
    }
}

print("Downloading Subway Cruelty scene images (Low-res 512x912 to bypass 402 Payment Required):")
for filename, info in prompts.items():
    prompt = info["prompt"]
    seed = info["seed"]
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Using 512x912 resolution to fit within free tier limits
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=912&nologo=true&seed={seed}"
    dest_path = os.path.join(dest_dir, filename)
    
    print(f"Downloading {filename} (Seed: {seed})...")
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

print("\nAll downloads completed!")
