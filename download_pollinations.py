import os
import urllib.request
import urllib.parse
import time

# Prompts mapping
prompts = {
    17: "A 16:9 cinematic shot. A cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes on his blue fur, a pink nose, and large glossy expressive eyes. He has bare blue ears and no beanie or hoodie. He is walking on a modern street in front of Gyeongbokgung palace gates at night. Pixar style, soft cinematic lighting. No text, no words.",
    18: "A 16:9 cinematic shot. A cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes, a pink nose, and large glossy expressive eyes. He has bare blue ears and no beanie or hoodie. He is standing in front of ancient Geoncheonggung palace ruins at night, staring blankly at a glowing smartphone in his paws. Ethereal, mysterious. Pixar style. No text.",
    19: "A 16:9 cinematic shot. Extreme close-up of the large, glossy, expressive eyes of a cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes. Reflected clearly in his big eyes are red flames and dark shadows of an ancient Joseon palace burning. Intense emotion, sadness. Pixar style. No text.",
    20: "A 16:9 cinematic shot. A cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes, a pink nose, and large glossy expressive eyes. He has bare blue ears and no beanie. He stands in the present day. A semi-transparent, pale, sorrowful ghost of an ancient Joseon Empress in a white Hanbok overlaps beautifully with the background. Ethereal, emotional, Pixar style. No text.",
    21: "A 16:9 cinematic shot. A cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes, a pink nose, and large glossy expressive eyes. He has bare blue ears and no beanie. He is looking shocked and heartbroken, his mouth slightly open in surprise. Pixar style, emotional. No text.",
    22: "A 16:9 cinematic shot. Extreme close-up of a cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes. His large, glossy, expressive eyes are filled with tears, sparkling under the moonlight. Deep sorrow, Pixar style. No text.",
    23: "A 16:9 cinematic shot. A cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes, a pink nose. He has bare blue ears. He is crying, covering his face with his blue paws in deep sorrow. Pixar style, emotional. No text.",
    24: "A 16:9 cinematic shot. A cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes, a pink nose. He is crying. A soft, semi-transparent ghost hand of the Joseon Empress is gently patting his head in a warm, comforting gesture. Ethereal, touching, Pixar style. No text.",
    25: "A 16:9 cinematic shot. A cute 3D cartoon blue Haetae (Korean monster) with black tiger stripes. He stands alone under a beautiful night sky filled with starlight and soft glowing constellations, looking peaceful yet sorrowful. Pixar style. No text.",
    30: "A 16:9 cinematic group portrait of the K-Demon Hunter characters: Duffy (a cute 3D cartoon blue Haetae monster with tiger stripes), Seo-ssi (a cool Korean exorcist in a long trench coat), Bobby (a hip foreigner holding a tablet), Heo Yong-jun (a calm doctor in a white doctor coat), and Kang Ha-ru (a warm middle-aged Korean man). They are standing side by side under a beautiful starry night sky, looking warmly towards the camera. Ethereal, emotional, Pixar 3D animated movie style, soft cinematic lighting. No text."
}

def download_image(cut_num, prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    # Using pollinations AI to bypass rate limit
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true&seed={cut_num + 2026}"
    
    if 17 <= cut_num <= 25:
        dest_dir = r"D:\DMDG_UT\YOUTUBE\result\webtoon_30cuts\Act3"
    elif cut_num == 30:
        dest_dir = r"D:\DMDG_UT\YOUTUBE\result\webtoon_30cuts\Act4"
    else:
        return
        
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, f"{cut_num:03d}_cut{cut_num}.png")
    
    print(f"Downloading Cut {cut_num}...")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            with open(dest_path, "wb") as f:
                f.write(response.read())
        print(f"Success: Saved to {dest_path}")
    except Exception as e:
        print(f"Failed to download Cut {cut_num}: {e}")

def main():
    for cut, prompt in prompts.items():
        download_image(cut, prompt)
        time.sleep(2) # rate limit politeness

if __name__ == "__main__":
    main()
