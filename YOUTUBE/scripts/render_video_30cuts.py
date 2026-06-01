import os
import subprocess

IMG_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\result\webtoon_30cuts"
AUDIO_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\result\audio\longform"
EXPORT_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\result\video_exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

languages = ["KOR", "ENG", "JPN"]

# Scene to Cut mapping
# Scene 1: Cut 1~5
# Scene 2: Cut 6~15
# Scene 3: Cut 16~25
# Scene 4: Cut 26~30
scene_mapping = {
    1: list(range(1, 6)),
    2: list(range(6, 16)),
    3: list(range(16, 26)),
    4: list(range(26, 31))
}

texts = {
    "KOR": [
        "1895년의 가을밤, 건청궁의 공기는 유난히 차가웠습니다.\n한 나라의 국모가 머무는 곳이었지만,\n그 밤의 정적은 다가올 비극을 예견하듯 무겁게 가라앉아 있었습니다.",
        "누구도 상상하지 못한 폭력이\n가장 깊은 궁궐의 문을 부수고 들어왔습니다.\n바닥에 떨어진 옥비녀 위로, 붉은 눈물이 번져갔습니다.",
        "그녀가 스러져간 그 자리에, 지금 우리는 서 있습니다.\n부당하게 빼앗긴 삶에 대한 슬픔은 국경을 넘어 우리의 마음을 울립니다.\n이것이 바로 우리가 나누어야 할 슬픔, '한(恨)'입니다.",
        "아픈 역사를 기억하는 가장 따뜻한 방법은,\n서로의 목소리로 그 슬픔을 안아주는 것입니다.\n누군가의 상처가 당신의 목소리로 치유될 수 있도록.\n고정댓글 링크를 눌러, 지금 당신의 목소리로 다음 글을 읽어주세요."
    ],
    "ENG": [
        "On an autumn night in 1895, the air around Geoncheonggung Palace was unusually cold.\nThough it was the residence of the nation's mother,\nthe silence of that night hung heavy, as if foreseeing the tragedy to come.",
        "Unimaginable violence shattered the doors of the deepest palace.\nUnder the guise of power and ambition, a human being's dignity was ruthlessly trampled.\nOver the jade hairpin fallen on the floor, red tears began to spread.",
        "In the very place where she fell, we stand today.\nThough our languages differ and our worlds are worlds apart,\nthe sorrow for a life unjustly taken resonates across borders, touching our hearts.\nThis is the shared sorrow we must embrace, the essence of Han.",
        "The warmest way to remember a painful history\nis to embrace that sorrow with each other's voices.\nSo that someone's wound might be healed by your voice.\nPlease click the link in the pinned comment to read the next line with your voice."
    ],
    "JPN": [
        "1895年の秋の夜、乾清宮の空気はひときわ冷たく感じられました。\n一国の国母が留まる場所でありながら、\nその夜の静寂はやがて訪れる悲劇を予見するかのように重く沈んでいました。",
        "誰も想像すらできなかった暴力が、最も奥深い宮殿の扉を打ち破って入り込みました。\n権力と野望という名の下に、一人の人間の尊厳が無惨にも踏みにじられました。\n床に落ちた玉の簪の上に、赤い涙が滲んでいきました。",
        "彼女が倒れたその場所に、今私たちは立っています。\n言葉が違い、生きてきた世界が違っても、不当に奪われた命への悲しみは国境を越えて私たちの心を打ちます。\nこれこそが、私たちが分かち合うべき悲しみ、ハンなのです。",
        "痛ましい歴史を記憶する最も温かい方法は、\nお互いの声でその悲しみを抱きしめることです。\n誰かの傷が、あなたの声によって癒やされるように。\n固定コメントのリンクをクリックして、あなたの声で次の文章を読んでください。"
    ]
}

def get_audio_duration(audio_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def create_ass(ass_path, text, duration):
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    cs = int((duration - int(duration)) * 100)
    end_time_str = f"{hours:d}:{minutes:02d}:{seconds:02d}.{cs:02d}"
    
    ass_text = text.replace('\n', '\\N')
    
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,50,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,100,100,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{end_time_str},Default,,0,0,0,,{ass_text}
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

def create_scene_video(image_paths, audio_path, ass_path, output_path, total_duration):
    print(f"Rendering {os.path.basename(output_path)}...")
    safe_ass_path = ass_path.replace("\\", "/").replace(":", "\\\\:")
    
    concat_txt_path = output_path.replace(".mp4", "_images.txt")
    img_duration = total_duration / len(image_paths)
    
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for img in image_paths:
            f.write(f"file '{img.replace(chr(92), '/')}'\n")
            f.write(f"duration {img_duration:.3f}\n")
        f.write(f"file '{image_paths[-1].replace(chr(92), '/')}'\n")

    is_scene4 = "scene4" in output_path.lower()
    
    filter_parts = [
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=20:20[bg]",
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=decrease[fg]",
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2[outv]"
    ]
    if is_scene4:
        filter_parts.append(f"[outv]subtitles='{safe_ass_path}',fade=out:st={total_duration - 2.0:.3f}:d=2.0[finalv]")
        filter_parts.append(f"[1:a]afade=out:st={total_duration - 2.0:.3f}:d=2.0[finala]")
        maps = ["-map", "[finalv]", "-map", "[finala]"]
    else:
        filter_parts.append(f"[outv]subtitles='{safe_ass_path}'[finalv]")
        maps = ["-map", "[finalv]", "-map", "1:a"]
        
    filter_complex_str = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_path, "-i", audio_path,
        "-filter_complex", filter_complex_str
    ] + maps + [
        "-c:v", "libx264", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-pix_fmt", "yuv420p", "-shortest", output_path
    ]
    subprocess.run(cmd)
    os.remove(concat_txt_path)

def main():
    concat_list_path = os.path.join(EXPORT_DIR, "concat_30cuts.txt")

    for lang in languages:
        print(f"\n--- Starting 30-cut {lang} version ---")
        output_final = os.path.join(EXPORT_DIR, f"longform_30cuts_{lang}_final.mp4")
        temp_files = []
        
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for scene_num in range(1, 5):
                # 오디오 파일 찾기
                audio_idx = (scene_num - 1) * 3 + 1
                if lang == "ENG": audio_idx += 1
                if lang == "JPN": audio_idx += 2
                audio_path = os.path.join(AUDIO_DIR, f"{audio_idx:03d}_long_scene{scene_num}_{lang}.mp3")
                
                if not os.path.exists(audio_path):
                    print(f"Audio missing: {audio_path}")
                    continue
                
                duration = get_audio_duration(audio_path)
                
                # 해당 씬에 속한 이미지 경로들 수집
                cuts = scene_mapping[scene_num]
                image_paths = []
                for c in cuts:
                    img = os.path.join(IMG_DIR, f"Act{scene_num}", f"{c:03d}_cut{c:02d}.png")
                    if os.path.exists(img):
                        image_paths.append(img)
                    else:
                        image_paths.append(os.path.join(EXPORT_DIR, "black.png"))
                
                if not image_paths:
                    print(f"No images found for Scene {scene_num}, skipping...")
                    continue
                
                temp_vid = os.path.join(EXPORT_DIR, f"temp_30c_scene{scene_num}_{lang}.mp4")
                temp_ass = os.path.join(EXPORT_DIR, f"temp_30c_scene{scene_num}_{lang}.ass")
                temp_files.extend([temp_vid, temp_ass])
                
                create_ass(temp_ass, texts[lang][scene_num-1], duration)
                create_scene_video(image_paths, audio_path, temp_ass, temp_vid, duration)
                
                f.write(f"file '{temp_vid.replace(chr(92), '/')}'\n")

            # 아웃트로 애니메이션 추가
            outro_path = os.path.join(EXPORT_DIR, "outro_anim.mp4")
            if os.path.exists(outro_path):
                f.write(f"file '{outro_path.replace(chr(92), '/')}'\n")

        print(f"Merging 30-cut {lang} version...")
        if os.path.getsize(concat_list_path) > 0:
            concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_final]
            subprocess.run(concat_cmd)
            print(f"Exported: {output_final}")
        else:
            print("No valid scenes rendered. Video export skipped.")

        for tf in temp_files:
            if os.path.exists(tf): os.remove(tf)
        if os.path.exists(concat_list_path): os.remove(concat_list_path)

if __name__ == "__main__":
    main()
