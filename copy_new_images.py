import glob, os, shutil

src_dir = r'C:\Users\tuesvonita\.gemini\antigravity\brain\2ee4d8d7-d6f4-4f6a-9967-53bd8300b878'
dest = r'D:\DMDG_UT\YOUTUBE\result\webtoon_30cuts\Act3'

for f in glob.glob(os.path.join(src_dir, 'cut_*_new*.png')):
    base = os.path.basename(f)
    num = int(base.split('_')[1])
    new_name = f"{num:03d}_cut{num}.png"
    shutil.copy(f, os.path.join(dest, new_name))
    print(f"Copied {base} to {new_name}")
