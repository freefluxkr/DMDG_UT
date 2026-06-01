import os
import subprocess

AUDIO_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\assets_audio"
EXPORT_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\exports"
IMG_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\assets_image"

os.makedirs(EXPORT_DIR, exist_ok=True)

# Define multiple images per scene for slideshow/animation cuts
IMG_HOOK1 = os.path.join(IMG_DIR, "subway_escalator_1.png")
IMG_HOOK2 = os.path.join(IMG_DIR, "subway_escalator_2.png")

IMG_SCENE1_1 = os.path.join(IMG_DIR, "subway_bump_1.png")
IMG_SCENE1_2 = os.path.join(IMG_DIR, "subway_bump_2.png")

IMG_SCENE2_1 = os.path.join(IMG_DIR, "subway_stairs_1.png")
IMG_SCENE2_2 = os.path.join(IMG_DIR, "subway_stairs_2.png")

IMG_SCENE3_1 = os.path.join(IMG_DIR, "subway_priority_seat_1.png")
IMG_SCENE3_2 = os.path.join(IMG_DIR, "subway_priority_seat_2.png")

IMG_OUTRO1 = os.path.join(IMG_DIR, "subway_screen_door_1.png")
IMG_OUTRO2 = os.path.join(IMG_DIR, "subway_screen_door_2.png")

languages = ["KOR", "ENG", "JPN"]

scenes = {
    "KOR": [
        {"audio": "001_subway_scene1_KOR.mp3", "images": [IMG_HOOK1, IMG_HOOK2], "text": "서울의 지하로 내려가는 건,\n거대한 콘크리트 위장에 삼켜지는 것과 비슷하다.\n그곳에는 특유의 메마른 규칙이 존재한다."},
        {"audio": "002_subway_scene2_KOR.mp3", "images": [IMG_SCENE1_1, IMG_SCENE1_2], "text": "사람들은 마찰력을 상실한 당구공처럼\n서로의 어깨를 퍽, 퍽 부딪치며 튕겨져 나간다.\n사과 같은 건 없다. 미안하다는 말은 사치품이니까."},
        {"audio": "003_subway_scene3_KOR.mp3", "images": [IMG_SCENE2_1, IMG_SCENE2_2], "text": "환승 계단 앞에서는 기묘한 집단 최면이 일어난다.\n연어 떼처럼 합류해 거대한 새치기의 강물을 만든다.\n줄을 서는 자만 어리석은 섬으로 남겨지는 기이한 풍경."},
        {"audio": "004_subway_scene4_KOR.mp3", "images": [IMG_SCENE3_1, IMG_SCENE3_2], "text": "경로석은 이어폰을 낀 젊은 귀족들의 차지다.\n눈을 감고 귀를 막으면,\n타인의 무게감은 완벽하게 증발해 버린다."},
        {"audio": "005_subway_outro_KOR.mp3", "images": [IMG_OUTRO1, IMG_OUTRO2], "text": "초속 100km로 달리는 도시.\n무언가 중요한 것을 승강장에 떨어뜨리고 온 것은 아닐까?\n\n여러분이 겪은 최악의 매너는? (댓글👇)"}
    ],
    "ENG": [
        {"audio": "001_subway_scene1_ENG.mp3", "images": [IMG_HOOK1, IMG_HOOK2], "text": "Descending into Seoul's underground is like\nbeing swallowed by a giant concrete stomach.\nA peculiar, dry set of rules exists there."},
        {"audio": "002_subway_scene2_ENG.mp3", "images": [IMG_SCENE1_1, IMG_SCENE1_2], "text": "People bounce off each other like frictionless\nbilliard balls, slamming shoulders.\nThere are no apologies. Saying 'sorry' is a luxury."},
        {"audio": "003_subway_scene3_ENG.mp3", "images": [IMG_SCENE2_1, IMG_SCENE2_2], "text": "A bizarre mass hypnosis occurs at the transfer stairs.\nCreating a massive river of line-cutters.\nOnly those who wait in line are left as fools."},
        {"audio": "004_subway_scene4_ENG.mp3", "images": [IMG_SCENE3_1, IMG_SCENE3_2], "text": "Priority seating belongs to young nobles\nwearing noise-canceling earphones.\nThe weight of others perfectly evaporates."},
        {"audio": "005_subway_outro_ENG.mp3", "images": [IMG_OUTRO1, IMG_OUTRO2], "text": "A city running at 100km/h.\nHave we dropped something crucial on the platform?\n\nWhat's your worst subway experience? (Comment👇)"}
    ],
    "JPN": [
        {"audio": "001_subway_scene1_JPN.mp3", "images": [IMG_HOOK1, IMG_HOOK2], "text": "ソウルの地下へ降りていくのは、巨大な\nコンクリートの胃袋に飲み込まれるようなものだ。\nそこには特有의 乾いたルールが存在する。"},
        {"audio": "002_subway_scene2_JPN.mp3", "images": [IMG_SCENE1_1, IMG_SCENE1_2], "text": "人々は摩擦を失ったビリヤード의 球のように、\n肩を激しくぶつけ合いながら弾き飛ばされる。\n謝罪などない。ごめんなさいという言葉は贅沢品だ。"},
        {"audio": "003_subway_scene3_JPN.mp3", "images": [IMG_SCENE2_1, IMG_SCENE2_2], "text": "乗り換え階段の前では、奇妙な集団催眠が起こる。\n巨大な割り込み의 川を作る。\n列に並ぶ者だけが愚かな島として取り残される風景。"},
        {"audio": "004_subway_scene4_JPN.mp3", "images": [IMG_SCENE3_1, IMG_SCENE3_2], "text": "優先席はノイズキャンセリングイヤホンをつけた\n若い貴族たちのものである。\n他人の重みはこの世界から完全に蒸発してしまう。"},
        {"audio": "005_subway_outro_JPN.mp3", "images": [IMG_OUTRO1, IMG_OUTRO2], "text": "秒速100kmで走る都市。\n何か重要なものをホームに落としてきたのではないか？\n\nあなたの最悪の地下鉄体験は？（コメント👇）"}
    ]
}

def get_audio_duration(audio_path):
    ffprobe_exe = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\ffprobe.exe"
    cmd = [
        ffprobe_exe, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        return float(res.stdout.strip())
    return 5.0

def create_ass(ass_path, text):
    ass_text = text.replace('\n', '\\N')
    # MarginV set to 300 to ensure subtitles stay inside safe area (above home indicator)
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,65,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,0,2,80,80,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,1:00:00.00,Default,,0,0,0,,{ass_text}
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

def create_image_video(image_path, duration, output_path):
    ffmpeg_exe = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\ffmpeg.exe"
    cmd = [
        ffmpeg_exe, "-y", "-loop", "1", "-i", image_path,
        "-t", f"{duration:.3f}",
        "-filter_complex", "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:20[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[outv]",
        "-map", "[outv]",
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-r", "30", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_scene_video(image_paths, audio_path, ass_path, output_path):
    print(f"Rendering {os.path.basename(output_path)}...")
    duration = get_audio_duration(audio_path)
    
    # Save current CWD and switch to EXPORT_DIR to avoid Windows drive letter colon parsing bug in ffmpeg filter graph
    orig_cwd = os.getcwd()
    os.chdir(EXPORT_DIR)
    
    segment_paths = []
    n = len(image_paths)
    seg_duration = duration / n
    
    for idx, img_path in enumerate(image_paths):
        current_dur = seg_duration if idx < n - 1 else (duration - seg_duration * idx)
        seg_vid_path = f"temp_seg_{idx}.mp4"
        create_image_video(img_path, current_dur, seg_vid_path)
        segment_paths.append(seg_vid_path)
        
    ffmpeg_exe = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\ffmpeg.exe"
    concat_txt_path = "temp_concat.txt"
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for seg in segment_paths:
            f.write(f"file '{seg}'\n")
            
    temp_visual = "temp_visual.mp4"
    concat_cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_path, "-c", "copy", temp_visual]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for seg in segment_paths:
        if os.path.exists(seg): os.remove(seg)
    if os.path.exists(concat_txt_path): os.remove(concat_txt_path)
    
    # Use only the filename of the subtitle (since we are in EXPORT_DIR)
    rel_ass_path = os.path.basename(ass_path)
    rel_output_path = os.path.basename(output_path)
    
    merge_cmd = [
        ffmpeg_exe, "-y", "-i", temp_visual, "-i", audio_path,
        "-vf", f"subtitles='{rel_ass_path}'",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", rel_output_path
    ]
    res = subprocess.run(merge_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg error merging subtitles/audio:\n{res.stderr}")
        
    if os.path.exists(temp_visual): os.remove(temp_visual)
    os.chdir(orig_cwd)

def main():
    concat_list_path = os.path.join(EXPORT_DIR, "shorts_concat.txt")
    ffmpeg_exe = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\ffmpeg.exe"

    for lang in languages:
        print(f"\n--- Starting {lang} Shorts version ---")
        output_final = os.path.join(EXPORT_DIR, f"subway_shorts_{lang}_final.mp4")
        temp_files = []
        
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for i, scene in enumerate(scenes[lang]):
                scene_num = i + 1
                audio_path = os.path.join(AUDIO_DIR, scene["audio"])
                temp_vid = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.mp4")
                
                if not os.path.exists(audio_path):
                    print(f"Missing audio: {audio_path}")
                    continue
                
                img_paths = scene["images"]
                temp_ass = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.ass")
                
                missing_img = False
                for img in img_paths:
                    if not os.path.exists(img):
                        print(f"Missing image: {img}")
                        missing_img = True
                        break
                if missing_img:
                    continue
                
                temp_files.extend([temp_vid, temp_ass])
                create_ass(temp_ass, scene["text"])
                create_scene_video(img_paths, audio_path, temp_ass, temp_vid)
                
                f.write(f"file '{temp_vid.replace(chr(92), '/')}'\n")

        print(f"Merging {lang} Shorts version...")
        concat_cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_final]
        res = subprocess.run(concat_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"FFmpeg merge error:\n{res.stderr}")

        for tf in temp_files:
            if os.path.exists(tf): os.remove(tf)
        if os.path.exists(concat_list_path): os.remove(concat_list_path)
            
        print(f"Exported Shorts video: {output_final}")

if __name__ == "__main__":
    main()
