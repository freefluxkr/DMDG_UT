import os
import urllib.request
import urllib.parse
import time

dest_dir = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Geumdeungjisa\assets_image"
os.makedirs(dest_dir, exist_ok=True)

# Lower resolutions (512x912 for vertical, 912x512 for horizontal) to bypass high-res 402 payment errors
prompts = {
    # 1. Shorts (Vertical, 512x912)
    "geumdeung_shorts_box.png": {
        "prompt": "A traditional Korean secret iron document box bound with a red silk cord, hidden in the dark wooden rafters of a Korean royal palace, dramatic shadows, mysterious atmosphere, modern Korean ink wash painting style, sumukhwa, highly detailed brush strokes, no text",
        "width": 512, "height": 912, "seed": 5001
    },
    "geumdeung_shorts_sad.png": {
        "prompt": "An elderly Joseon king in a red robe crying in agonizing regret inside a dark palace during a heavy thunderstorm, a silhouette of a large wooden rice chest (Duiju) in the background lit by lightning, modern Korean ink wash painting style, sumukhwa, deep dark mood, tragic, high contrast, no text",
        "width": 512, "height": 912, "seed": 5002
    },
    "geumdeung_shorts_write.png": {
        "prompt": "Close-up of an old king's hand writing secret Korean letters on a traditional scroll using a brush with dark red ink, illuminated by a single flickering candlelight, dark background, intense focus, Korean ink wash painting style, sumukhwa, no text",
        "width": 512, "height": 912, "seed": 5003
    },
    "geumdeung_shorts_jeongjo.png": {
        "prompt": "A young, determined Joseon King Jeongjo in royal red dragon robe (Gonryongpo) holding open a secret blood-stained scroll to confront terrified royal officials, dramatic low-angle shot, intense eye contact, Korean ink wash painting style, sumukhwa, historical epic, no text",
        "width": 512, "height": 912, "seed": 5004
    },
    
    # 2. Longform (Horizontal, 912x512)
    "geumdeung_long_throne.png": {
        "prompt": "The royal court of Joseon palace, empty and dark, dramatic lighting, foggy atmosphere, modern Korean ink wash painting style, sumukhwa, high contrast, fine brush strokes, 16:9 aspect ratio, no text",
        "width": 912, "height": 512, "seed": 6001
    },
    "geumdeung_long_tragedy.png": {
        "prompt": "A silhouette of a prince locked inside a wooden rice chest under the hot sun in the palace courtyard, dark shadows, tragic and heavy mood, modern Korean ink wash painting style, sumukhwa, no text",
        "width": 912, "height": 512, "seed": 6002
    },
    "geumdeung_long_blood.png": {
        "prompt": "Elderly Joseon King Yeongjo writing his secret confession on a white silk cloth with red blood-ink, tears in his eyes, candlelight illumination, modern Korean ink wash painting style, sumukhwa, high detail, no text",
        "width": 912, "height": 512, "seed": 6003
    },
    "geumdeung_long_hiding.png": {
        "prompt": "A loyal palace eunuch secretly hiding a small iron box inside the wooden column of the royal shrine at night, shadows, secrecy, modern Korean ink wash painting style, sumukhwa, no text",
        "width": 912, "height": 512, "seed": 6004
    },
    "geumdeung_long_lightning.png": {
        "prompt": "A violent thunderstorm over the Joseon royal shrine, a flash of bright lightning striking the roof and exposing the hidden metal box inside the cracked wooden pillar, modern Korean ink wash painting style, sumukhwa, epic scale, no text",
        "width": 912, "height": 512, "seed": 6005
    },
    "geumdeung_long_triumph.png": {
        "prompt": "King Jeongjo standing tall and proud in his dragon robe, holding a dusty secret scroll in the main palace hall, looking victorious and emotional, modern Korean ink wash painting style, sumukhwa, high detail, no text",
        "width": 912, "height": 512, "seed": 6006
    }
}

print("Downloading Geumdeungjisa scene images from Pollinations Free API (No Flux constraint, Lower-res):")
for filename, info in prompts.items():
    prompt = info["prompt"]
    width = info["width"]
    height = info["height"]
    seed = info["seed"]
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={seed}"
    dest_path = os.path.join(dest_dir, filename)
    
    print(f"Downloading {filename} ({width}x{height}, Seed: {seed})...")
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

print("\nGeumdeungjisa downloads completed!")
