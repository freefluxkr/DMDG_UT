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
        "prompt": "A traditional Korean secret iron document box bound with a red silk cord, hidden in the dark wooden rafters of a Joseon royal palace, traditional Korean Hanok architecture with Giwa tiled roof, dramatic shadows, mysterious atmosphere, modern Korean ink wash painting style, sumukhwa, highly detailed brush strokes, no text",
        "width": 512, "height": 912, "seed": 9201
    },
    "geumdeung_shorts_sad.png": {
        "prompt": "An elderly Joseon Dynasty King Yeongjo with a short grey beard, wearing a traditional Korean royal red robe (Gonryongpo) featuring circular golden dragon emblems embroidered on the shoulders and chest, and wearing a black royal hat with two tall upward-pointing wings at the back (Ikseongwan). Crying in agonizing regret. In the background, a silhouette of a large Korean wooden rice chest (Duiju), traditional Korean wooden doors with simple square grid paper screens (Changhoji). Strictly Korean face and historical dress, no Chinese Hanfu, no long Chinese braids, no Ming Dynasty hats. Modern Korean ink wash painting style, sumukhwa, tragic, high contrast, no text",
        "width": 512, "height": 912, "seed": 9202
    },
    "geumdeung_shorts_write.png": {
        "prompt": "Close-up of an old Joseon king's hand writing secret Korean Hangul characters on a traditional mulberry paper scroll using a brush with dark red ink, illuminated by a single flickering candlelight, dark background, intense focus, Korean ink wash painting style, sumukhwa, no text",
        "width": 512, "height": 912, "seed": 9203
    },
    "geumdeung_shorts_jeongjo.png": {
        "prompt": "A young, determined Joseon King Jeongjo with a clean-shaven Korean face, wearing a traditional Korean royal red robe with circular golden dragon patches on the chest and shoulders, and wearing a black royal cap with two upward wings at the back (Ikseongwan). He holds open a secret blood-stained scroll, confronting terrified royal officials who are kneeling on the wooden floor wearing traditional single-colored green official robes (Dallyeong) and black rounded hats with flat horizontal wings extending to the sides (Samo). Strictly Joseon Dynasty Korea royal hall, traditional Korean architecture with simple grid paper sliding screens, no Chinese high collars, no Chinese braids, no Ming Dynasty hats. Korean ink wash painting style, sumukhwa, historical epic, no text",
        "width": 512, "height": 912, "seed": 9204
    },
    
    # 2. Longform (Horizontal, 912x512)
    "geumdeung_long_throne.png": {
        "prompt": "The empty royal court hall of a Joseon Dynasty palace in Korea, traditional Korean Dancheong paint patterns on wooden pillars, simple grid patterned paper screens, dramatic lighting, foggy atmosphere, modern Korean ink wash painting style, sumukhwa, high contrast, 16:9 aspect ratio, no text",
        "width": 912, "height": 512, "seed": 9301
    },
    "geumdeung_long_tragedy.png": {
        "prompt": "A silhouette of a Joseon prince locked inside a traditional Korean wooden rice chest (Duiju) under the hot sun in the palace courtyard, dark shadows, tragic and heavy mood, traditional Korean Joseon architecture with Giwa roofs in background, modern Korean ink wash painting style, sumukhwa, no text",
        "width": 912, "height": 512, "seed": 9302
    },
    "geumdeung_long_blood.png": {
        "prompt": "Elderly Joseon King Yeongjo in red royal Gonryongpo robe with circular golden dragon patches and black Ikseongwan cap, writing his secret confession on a white silk cloth with red blood-ink, tears in his eyes, candlelight illumination, Joseon Dynasty Korea style, strictly Korean dress and features, no Chinese Hanfu, modern Korean ink wash painting style, sumukhwa, high detail, no text",
        "width": 912, "height": 512, "seed": 9303
    },
    "geumdeung_long_hiding.png": {
        "prompt": "A loyal palace eunuch in green Joseon Dynasty eunuch robe secretly hiding a small iron box inside the wooden column of the royal shrine at night, shadows, secrecy, modern Korean ink wash painting style, sumukhwa, no text",
        "width": 912, "height": 512, "seed": 9304
    },
    "geumdeung_long_lightning.png": {
        "prompt": "A violent thunderstorm over the Joseon royal shrine (Jongmyo) with traditional Korean Giwa roofs, a flash of bright lightning striking the roof and exposing the hidden metal box inside the cracked wooden pillar, modern Korean ink wash painting style, sumukhwa, epic scale, no text",
        "width": 912, "height": 512, "seed": 9305
    },
    "geumdeung_long_triumph.png": {
        "prompt": "King Jeongjo standing tall and proud in his red royal dragon robe (Gonryongpo) and royal Ikseongwan hat, holding a dusty secret scroll in the main palace hall, looking victorious and emotional, Joseon Dynasty royal hall, strictly Korean historical style, modern Korean ink wash painting style, sumukhwa, high detail, no text",
        "width": 912, "height": 512, "seed": 9306
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
