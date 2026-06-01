import os
import subprocess

IMG_DIR = r"d:\DMDG_UT\YOUTUBE\result\webtoon"
AUDIO_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\shorts"
EXPORT_DIR = r"d:\DMDG_UT\YOUTUBE\result\video_exports"

languages = ["KOR", "ENG", "JPN"]

scenes = {
    "KOR": [
        {"audio": "001_shorts_scene1_duffy_KOR.mp3", "image": "003_scene3.png", "text": "오 마이 갓... 인간들은 왜 이렇게 아름다운 궁궐에서\n이런 끔찍하고 소름 돋는 무거운 감정을 느끼는 거죠?\n이게 너희가 말하는 '한'인가요?"},
        {"audio": "002_shorts_scene2_duffy_KOR.mp3", "image": "001_scene1.png", "text": "진짜 이해할 수 없어...\n어? 뭐지?"},
        {"audio": "003_shorts_scene2_voice_KOR.mp3", "image": "001_scene1.png", "text": "그 밤, 조선의 국모는 가장 차가운 칼날 앞에 섰지만,\n그녀의 마지막 시선은..."},
        {"audio": "004_shorts_scene3_duffy_KOR.mp3", "image": "002_scene2.png", "text": "와우. 이 슬픔은... 차원을 넘어선 무언가네요.\n대체 이 목소리는 누구죠?"},
        {"audio": "005_shorts_scene4_narration_KOR.mp3", "image": "black", "text": "신수 해태마저 울린 이 목소리의 정체와,\n숨겨진 조선의 마지막 밤 이야기...\n\n본편 롱폼 영상에서 확인하세요!"}
    ],
    "ENG": [
        {"audio": "001_shorts_scene1_duffy_ENG.mp3", "image": "003_scene3.png", "text": "Oh my god... Why do humans feel such a terrifying and\nheavy emotion in such a beautiful palace?\nIs this what you call 'Han'?"},
        {"audio": "002_shorts_scene2_duffy_ENG.mp3", "image": "001_scene1.png", "text": "I really can't understand...\nHuh? What is this?"},
        {"audio": "003_shorts_scene2_voice_ENG.mp3", "image": "001_scene1.png", "text": "That night, the mother of Joseon stood before the coldest blade,\nbut her final gaze was..."},
        {"audio": "004_shorts_scene3_duffy_ENG.mp3", "image": "002_scene2.png", "text": "Wow. This sorrow... it's something beyond dimensions.\nWhose voice is this?"},
        {"audio": "005_shorts_scene4_narration_ENG.mp3", "image": "black", "text": "The true identity of the voice that moved Haetae,\nand the hidden story of Joseon's final night...\n\nWatch the full video now!"}
    ],
    "JPN": [
        {"audio": "001_shorts_scene1_duffy_JPN.mp3", "image": "003_scene3.png", "text": "オーマイゴッド…人間たちはなぜ、こんなに美しい宮殿で\nこんなにも恐ろしくて重い感情を抱くの？\nこれが君たちの言う「ハン」なの？"},
        {"audio": "002_shorts_scene2_duffy_JPN.mp3", "image": "001_scene1.png", "text": "本当に理解できない…\nえ？何これ？"},
        {"audio": "003_shorts_scene2_voice_JPN.mp3", "image": "001_scene1.png", "text": "その夜、朝鮮の国母は最も冷たい刃の前に立ったが、\n彼女の最後の視線は…"},
        {"audio": "004_shorts_scene3_duffy_JPN.mp3", "image": "002_scene2.png", "text": "ワオ。この悲しみは…次元を超えた何かだね。\n一体この声は誰なの？"},
        {"audio": "005_shorts_scene4_narration_JPN.mp3", "image": "black", "text": "神獣ヘテさえも泣かせたこの声の正体と、\n隠された朝鮮の最後の夜の物語…\n\n本編のロング動画でご確認ください！"}
    ]
}

def create_ass(ass_path, text):
    ass_text = text.replace('\n', '\\N')
    
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,65,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,80,80,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,1:00:00.00,Default,,0,0,0,,{ass_text}
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

def create_scene_video(image_path, audio_path, ass_path, output_path):
    print(f"Rendering {os.path.basename(output_path)}...")
    safe_ass_path = ass_path.replace("\\", "/").replace(":", "\\\\:")
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", image_path, "-i", audio_path,
        "-filter_complex", f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:20[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[outv];[outv]subtitles='{safe_ass_path}'[finalv]",
        "-map", "[finalv]", "-map", "1:a",
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_scrolling_scene(audio_path, text, temp_txt_path, output_path):
    print(f"Rendering SCROLLING SCENE {os.path.basename(output_path)}...")
    with open(temp_txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    safe_txt_path = temp_txt_path.replace("\\", "/").replace(":", "\\\\:")
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:r=30", "-i", audio_path,
        "-vf", f"drawtext=fontfile='C\\:\\\\Windows\\\\Fonts\\\\malgun.ttf':textfile='{safe_txt_path}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-t*200:line_spacing=30:alpha='if(lt(t,1),0,if(lt(t,2),t-1,1))'",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    concat_list_path = os.path.join(EXPORT_DIR, "shorts_concat.txt")

    for lang in languages:
        print(f"\n--- Starting {lang} Shorts version ---")
        output_final = os.path.join(EXPORT_DIR, f"shorts_teaser_{lang}_with_subs.mp4")
        temp_files = []
        
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for i, scene in enumerate(scenes[lang]):
                scene_num = i + 1
                audio_path = os.path.join(AUDIO_DIR, scene["audio"])
                temp_vid = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.mp4")
                
                if not os.path.exists(audio_path): continue
                
                if scene["image"] != "black":
                    image_path = os.path.join(IMG_DIR, scene["image"])
                    temp_ass = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.ass")
                    if not os.path.exists(image_path): continue
                    
                    temp_files.extend([temp_vid, temp_ass])
                    create_ass(temp_ass, scene["text"])
                    create_scene_video(image_path, audio_path, temp_ass, temp_vid)
                else:
                    temp_txt = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.txt")
                    temp_files.extend([temp_vid, temp_txt])
                    create_scrolling_scene(audio_path, scene["text"], temp_txt, temp_vid)
                
                f.write(f"file '{temp_vid.replace(chr(92), '/')}'\n")

        print(f"Merging {lang} Shorts version...")
        concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_final]
        subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for tf in temp_files:
            if os.path.exists(tf): os.remove(tf)
        if os.path.exists(concat_list_path): os.remove(concat_list_path)
            
        print(f"Exported Shorts video: {output_final}")

if __name__ == "__main__":
    main()
