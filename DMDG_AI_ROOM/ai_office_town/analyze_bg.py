import sys
from PIL import Image

def analyze_bg(filename):
    try:
        img = Image.open(filename).convert("RGBA")
        pixels = img.load()
        width, height = img.size
        
        # Check corners to see background colors
        corners = [
            (0, 0), (width-1, 0), (0, height-1), (width-1, height-1),
            (0, 10), (10, 0)
        ]
        colors = set()
        for x, y in corners:
            colors.add(pixels[x, y])
            
        print(f"File: {filename}")
        print(f"Corner colors: {colors}")
    except Exception as e:
        print(f"Error analyzing {filename}: {e}")

analyze_bg("assets/images/Satya_Nadella.png")
analyze_bg("assets/images/Craig_Federighi.png")
analyze_bg("assets/images/Hans_Zimmer.png")
