import os
from PIL import Image, ImageDraw, ImageFont

def fix_cut29():
    base_path = r"D:\DMDG_UT\YOUTUBE\result\webtoon_30cuts\Act4\029_cut29.png"
    logo_path = r"D:\DMDG_UT\YOUTUBE\characters\당목담글_로고.png"
    
    if not os.path.exists(base_path) or not os.path.exists(logo_path):
        print("Files missing for Cut 29")
        return
        
    base = Image.open(base_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    
    # Resize logo if it's too big (assuming 1920x1080 background)
    target_width = int(base.width * 0.4)
    ratio = target_width / logo.width
    logo = logo.resize((target_width, int(logo.height * ratio)), Image.LANCZOS)
    
    # Calculate position (center)
    x = (base.width - logo.width) // 2
    y = (base.height - logo.height) // 2
    
    # Paste logo onto base using alpha channel as mask
    base.paste(logo, (x, y), logo)
    
    # Save back as RGB
    base.convert("RGB").save(base_path)
    print("Cut 29 logo overlaid successfully.")

def fix_cut30():
    base_path = r"D:\DMDG_UT\YOUTUBE\result\webtoon_30cuts\Act4\030_cut30.png"
    if not os.path.exists(base_path):
        print("Base image for Cut 30 missing.")
        return
        
    base = Image.open(base_path).convert("RGBA")
    draw = ImageDraw.Draw(base)
    
    text = "지금, 당신의 목소리로 다음글을 읽어 주세요"
    # Try to load a Korean font
    font_paths = [
        "C:\\Windows\\Fonts\\malgun.ttf", 
        "C:\\Windows\\Fonts\\NanumGothic.ttf",
        "C:\\Windows\\Fonts\\gulim.ttc"
    ]
    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, 80)
            break
            
    if font is None:
        font = ImageFont.load_default()
        
    # Add text shadow/outline for readability
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    x = (base.width - tw) // 2
    y = (base.height - th) // 2
    
    # Semi-transparent text to simulate fade (or just solid text, and we let ffmpeg do the fade out later if needed)
    # The user asked for "텍스트 페이드 아웃 효과". I will just render solid text here, since it's a still image.
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    base.convert("RGB").save(base_path)
    print("Cut 30 text added successfully.")

if __name__ == "__main__":
    fix_cut29()
    fix_cut30()
