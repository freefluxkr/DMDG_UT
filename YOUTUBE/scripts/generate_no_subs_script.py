import os
import subprocess

with open(r'D:\DMDG_UT\YOUTUBE\render_video.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(",subtitles='{safe_srt_path}':force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=30'", "")
code = code.replace("longform_{lang}_preview_with_subs.mp4", "longform_{lang}_preview_no_subs.mp4")
code = code.replace('languages = ["KOR", "ENG", "JPN"]', 'languages = ["ENG", "JPN"]')

with open(r'D:\DMDG_UT\YOUTUBE\render_no_subs.py', 'w', encoding='utf-8') as f:
    f.write(code)
