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
    font_paths = [
        "C:\\Windows\\Fonts\\malgun.ttf", 
        "C:\\Windows\\Fonts\\NanumGothic.ttf",
        "C:\\Windows\\Fonts\\gulim.ttc"
    ]
    
    # Dynamically find a font size that fits 90% of image width
    target_width = int(base.width * 0.9)
    font_size = 80
    font = None
    
    while font_size > 10:
        found_font = None
        for fp in font_paths:
            if os.path.exists(fp):
                found_font = ImageFont.truetype(fp, font_size)
                break
        if not found_font:
            found_font = ImageFont.load_default()
            font = found_font
            break
            
        bbox = draw.textbbox((0,0), text, font=found_font)
        tw = bbox[2] - bbox[0]
        if tw <= target_width:
            font = found_font
            break
        font_size -= 2
        
    if font is None:
        font = ImageFont.load_default()
        
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    x = (base.width - tw) // 2
    y = int(base.height * 0.8) - th  # Position at bottom-middle area (around 80% height)
    
    # Draw white text with black outline for maximum legibility
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    
    base.convert("RGB").save(base_path)
    print(f"Cut 30 text added successfully (size={font_size}).")

if __name__ == "__main__":
    fix_cut29()
    fix_cut30()
