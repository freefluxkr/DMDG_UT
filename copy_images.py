import glob, os, shutil

src_dir = r'C:\Users\tuesvonita\.gemini\antigravity\brain\2ee4d8d7-d6f4-4f6a-9967-53bd8300b878'
dest_act3 = r'D:\DMDG_UT\YOUTUBE\result\webtoon_30cuts\Act3'
dest_act4 = r'D:\DMDG_UT\YOUTUBE\result\webtoon_30cuts\Act4'

os.makedirs(dest_act3, exist_ok=True)
os.makedirs(dest_act4, exist_ok=True)

for f in glob.glob(os.path.join(src_dir, 'cut*.png')):
    base = os.path.basename(f)
    # base is like cut16_12345.png
    num_str = base.split('_')[0].replace('cut', '')
    if not num_str.isdigit():
        continue
    num = int(num_str)
    
    if num >= 16 and num <= 25:
        dest_dir = dest_act3
    elif num >= 26 and num <= 30:
        dest_dir = dest_act4
    else:
        continue
        
    new_name = f"{num:03d}_cut{num}.png"
    shutil.copy(f, os.path.join(dest_dir, new_name))
    print(f"Copied {base} to {new_name}")
