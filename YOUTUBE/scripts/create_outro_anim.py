import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

EXPORT_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\result\video_exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def create_frames(lang):
    width, height = 1920, 1080
    
    try:
        font_sub = ImageFont.truetype("malgun.ttf", 80)
        font_heart = ImageFont.truetype("malgun.ttf", 120)
    except:
        font_sub = ImageFont.load_default()
        font_heart = font_sub

    texts = {
        "KOR": "화면을 두 번 터치해 보세요!",
        "ENG": "Please double tap the screen!",
        "JPN": "画面を2回タッチしてみてください！"
    }
    text_touch = texts.get(lang, texts["KOR"])
    
    # Load the 30th cut image as background
    bg_path = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\result\webtoon_30cuts\Act4\030_cut30.png"
    if os.path.exists(bg_path):
        base_bg = Image.open(bg_path).convert('RGB')
        # Resize/crop to 1920x1080
        img_w, img_h = base_bg.size
        ratio = max(width/img_w, height/img_h)
        new_w, new_h = int(img_w * ratio), int(img_h * ratio)
        base_bg = base_bg.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        base_bg = base_bg.crop((left, top, left + width, top + height))
        
        # Add a dark overlay to make text pop
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 150))
        base_bg.paste(overlay, (0, 0), overlay)
    else:
        base_bg = Image.new('RGB', (width, height), color=(20, 20, 20))
    
    # Frame 1: Empty heart
    img1 = base_bg.copy()
    d1 = ImageDraw.Draw(img1)
    
    # Draw text centered
    d1.text((width//2, height//2 - 50), text_touch, fill=(255, 200, 200), font=font_sub, anchor="mm")
    d1.text((width//2, height//2 + 150), "♡", fill=(255, 255, 255), font=font_heart, anchor="mm")
    
    frame1_path = os.path.join(EXPORT_DIR, f"outro_frame1_{lang}.png")
    img1.save(frame1_path)

    # Frame 2: Filled heart (red)
    img2 = base_bg.copy()
    d2 = ImageDraw.Draw(img2)
    d2.text((width//2, height//2 - 50), text_touch, fill=(255, 200, 200), font=font_sub, anchor="mm")
    d2.text((width//2, height//2 + 150), "♥", fill=(255, 0, 0), font=font_heart, anchor="mm")
    
    frame2_path = os.path.join(EXPORT_DIR, f"outro_frame2_{lang}.png")
    img2.save(frame2_path)
    
    return frame1_path, frame2_path

def render_anim(lang, frame1, frame2):
    out_mp4 = os.path.join(EXPORT_DIR, f"outro_anim_{lang}.mp4")
    
    # Create a text file for ffmpeg concat to loop the images
    concat_txt = os.path.join(EXPORT_DIR, f"outro_concat_{lang}.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for _ in range(3): # loop 3 times (3 seconds total if 0.5s each)
            f.write(f"file '{frame1.replace(chr(92), '/')}'\n")
            f.write("duration 0.5\n")
            f.write(f"file '{frame2.replace(chr(92), '/')}'\n")
            f.write("duration 0.5\n")
        # last frame needs to be written again without duration for concat demuxer
        f.write(f"file '{frame2.replace(chr(92), '/')}'\n")

    ffmpeg_exe = os.path.join(r"c:\Users\user\Documents\DMDG_UT", "YOUTUBE", "ffmpeg.exe")
    cmd = [
        ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-shortest", out_mp4
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error creating outro: {result.stderr}")
    
    os.remove(concat_txt)
    os.remove(frame1)
    os.remove(frame2)
    print(f"Created {out_mp4}")

if __name__ == "__main__":
    for lang in ["KOR", "ENG", "JPN"]:
        f1, f2 = create_frames(lang)
        render_anim(lang, f1, f2)
