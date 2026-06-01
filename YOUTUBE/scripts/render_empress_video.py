import os
import subprocess

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
IMG_DIR = os.path.join(BASE_DIR, r"YOUTUBE\result\webtoon_30cuts")
AUDIO_DIR = os.path.join(BASE_DIR, r"YOUTUBE\Projects\Empress_Longform\assets_audio")
EXPORT_DIR = os.path.join(BASE_DIR, r"YOUTUBE\Projects\Empress_Longform\exports")

os.makedirs(EXPORT_DIR, exist_ok=True)

languages = ["KOR", "ENG", "JPN"]

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
        "그녀가 스러져간 그 자리에, 지금 우리는 서 있습니다.\n수많은 계절이 바뀌고 백 년의 세월이 흘렀지만, 그날 밤 흩날리던 슬픔의 조각들은 여전히 이 궁궐 어귀에 남아 있습니다.\n언어가 다르고 살아온 세상이 달라도, 부당하게 빼앗긴 삶에 대한 아픔은 국경을 넘어 우리의 마음을 울립니다.\n이 깊은 먹먹함, 이토록 찬란하고도 서글픈 공감대... 이것이 바로 우리가 함께 나누고 위로해야 할 조선의 슬픔, '한(恨)'입니다.",
        "아픈 역사를 기억하는 가장 따뜻한 방법은 무엇일까요?\n그것은 바로 서로의 목소리로, 과거의 멍든 슬픔을 조용히 안아주는 것입니다.\n누군가의 깊은 상처가, 오늘을 살아가는 당신의 따뜻한 목소리로 치유될 수 있도록.\n이제는 당신이 이 이야기의 화자가 되어주실 차례입니다.\n지금 화면을 두 번 터치하여 당신의 목소리로 다음 글을 읽어주세요."
    ],
    "ENG": [
        "On an autumn night in 1895, the air around Geoncheonggung Palace was unusually cold.\nThough it was the residence of the nation's mother,\nthe silence of that night hung heavy, as if foreseeing the tragedy to come.",
        "Unimaginable violence shattered the doors of the deepest palace.\nUnder the guise of power and ambition, a human being's dignity was ruthlessly trampled.\nOver the jade hairpin fallen on the floor, red tears began to spread.",
        "In the very place where she fell, we stand today.\nCountless seasons have passed and a century has flowed by, yet the fragments of sorrow scattered that night still linger at the edge of this palace.\nThough our languages differ and our worlds are worlds apart, the pain of a life unjustly taken resonates across borders, touching our hearts.\nThis deep profoundness, this brilliantly sorrowful empathy... This is the shared sorrow of Joseon we must comfort together, the essence of 'Han'.",
        "What is the warmest way to remember a painful history?\nIt is to embrace the bruised sorrow of the past quietly with each other's voices.\nSo that someone's deep wound might be healed by your warm voice living today.\nNow, it is your turn to become the narrator of this story.\nPlease double tap the screen right now and read the next line with your voice."
    ],
    "JPN": [
        "1895年の秋の夜、乾清宮の空気はひときわ冷たく感じられました。\n一国の国母が留まる場所でありながら、\nその夜の静寂はやがて訪れる悲劇を予見するかのように重く沈んでいました。",
        "誰も想像すらできなかった暴力が、最も奥深い宮殿の扉を打ち破って入り込みました。\n権力と野望という名の下に、一人の人間の尊厳が無惨にも踏みにじられました。\n床に落ちた玉の簪の上に、赤い涙が滲んでいきました。",
        "彼女が倒れたその場所に、今私たちは立っています。\n数え切れないほどの季節が巡り、百年の歳月が流れましたが、あの夜に散った悲しみのかけらは、未だにこの宮殿の片隅に残っています。\n言葉が違い、生きてきた世界が違っても、不当に奪われた命への痛みは国境を越えて私たちの心を打ちます。\nこの深い胸の詰まり、これほどまでに美しくも切ない共感… これこそが、私たちが共に分かち合い慰め合うべき朝鮮の悲しみ、「恨（ハン）」なのです。",
        "痛ましい歴史を記憶する最も温かい方法は何でしょうか？\nそれは、お互いの声で、過去の傷ついた悲しみを静かに抱きしめることです。\n誰かの深い傷が、今日を生きるあなたの温かい声によって癒やされるように。\n今度は、あなたがこの物語の語り手になる番です。\n今すぐ画面を2回タッチして、あなたの声で次の文章を読んでください。"
    ]
}

def get_audio_duration(audio_path):
    ffprobe_exe = os.path.join(BASE_DIR, "YOUTUBE", "ffprobe.exe")
    cmd = [ffprobe_exe, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def create_ass(ass_path, text, duration):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    num_lines = len(lines)
    
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
"""
    if num_lines > 0:
        total_chars = sum(len(line) for line in lines)
        current_time = 0.0
        
        for line in lines:
            if total_chars == 0:
                line_duration = duration / num_lines
            else:
                line_duration = duration * (len(line) / total_chars)
                
            start_time = current_time
            end_time = current_time + line_duration
            current_time = end_time
            
            def format_time(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                cs = int((t - int(t)) * 100)
                return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"
                
            ass_content += f"Dialogue: 0,{format_time(start_time)},{format_time(end_time)},Default,,0,0,0,,{line}\n"

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
    
    # Use relative path for subtitles to avoid Windows drive letter colon parsing bug in ffmpeg filter graph
    rel_ass = os.path.basename(ass_path)
    if is_scene4:
        filter_parts.append(f"[outv]subtitles='{rel_ass}',fade=out:st={total_duration - 2.0:.3f}:d=2.0[finalv]")
        maps = ["-map", "[finalv]", "-map", "1:a"]
    else:
        filter_parts.append(f"[outv]subtitles='{rel_ass}'[finalv]")
        maps = ["-map", "[finalv]", "-map", "1:a"]
        
    filter_complex_str = ";".join(filter_parts)

    concat_txt_path_safe = concat_txt_path.replace(chr(92), "/")
    audio_path_safe = audio_path.replace(chr(92), "/")
    output_path_safe = output_path.replace(chr(92), "/")
    
    ffmpeg_exe = os.path.join(BASE_DIR, "YOUTUBE", "ffmpeg.exe")
    cmd = [
        ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_path_safe, "-i", audio_path_safe,
        "-filter_complex", filter_complex_str
    ] + maps + [
        "-c:v", "libx264", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-pix_fmt", "yuv420p", "-shortest", output_path_safe
    ]
    # 병합 에러 방지를 위해 에러 출력 (cwd를 EXPORT_DIR로 설정하여 자막 상대경로 인식)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=EXPORT_DIR)
    if result.returncode != 0:
        print(f"Error in create_scene_video: {result.stderr}")
        with open(os.path.join(EXPORT_DIR, "ffmpeg_error_log.txt"), "w", encoding="utf-8") as errf:
            errf.write("CMD: " + " ".join(cmd) + "\n\n")
            errf.write("STDERR:\n" + result.stderr)
        print("Check ffmpeg_error_log.txt for detailed error.")
    os.remove(concat_txt_path)

def main():
    concat_list_path = os.path.join(EXPORT_DIR, "concat_empress_30cuts.txt")

    for lang in languages:
        print(f"\n--- Starting 30-cut {lang} version ---")
        output_final = os.path.join(EXPORT_DIR, f"longform_30cuts_{lang}_final.mp4")
        temp_files = []
        
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for scene_num in range(1, 5):
                audio_idx = (scene_num - 1) * 3 + 1
                if lang == "ENG": audio_idx += 1
                if lang == "JPN": audio_idx += 2
                
                # 새로운 폴더 구조 기반 오디오 경로
                audio_path = os.path.join(AUDIO_DIR, f"{audio_idx:03d}_long_scene{scene_num}_{lang}_mixed.mp3")
                
                if not os.path.exists(audio_path):
                    print(f"Audio missing: {audio_path}")
                    continue
                
                duration = get_audio_duration(audio_path)
                
                cuts = scene_mapping[scene_num]
                image_paths = []
                for c in cuts:
                    img = os.path.join(IMG_DIR, f"Act{scene_num}", f"{c:03d}_cut{c:02d}.png")
                    if os.path.exists(img):
                        image_paths.append(img)
                    else:
                        image_paths.append(os.path.join(BASE_DIR, r"YOUTUBE\result\video_exports\black.png"))
                
                if not image_paths:
                    continue
                
                temp_vid = os.path.join(EXPORT_DIR, f"temp_30c_scene{scene_num}_{lang}.mp4")
                temp_ass = os.path.join(EXPORT_DIR, f"temp_30c_scene{scene_num}_{lang}.ass")
                temp_files.extend([temp_vid, temp_ass])
                
                create_ass(temp_ass, texts[lang][scene_num-1], duration)
                create_scene_video(image_paths, audio_path, temp_ass, temp_vid, duration)
                
                f.write(f"file '{temp_vid.replace(chr(92), '/')}'\n")

            # 아웃트로가 없으면 그냥 무시하고 지금까지 만든 Scene들만 병합
            outro_path = os.path.join(BASE_DIR, rf"YOUTUBE\result\video_exports\outro_anim_{lang}.mp4")
            if os.path.exists(outro_path):
                f.write(f"file '{outro_path.replace(chr(92), '/')}'\n")
            
        print(f"Merging {lang} version to final...")
        if os.path.getsize(concat_list_path) > 0:
            ffmpeg_exe = os.path.join(BASE_DIR, "YOUTUBE", "ffmpeg.exe")
            concat_cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_final]
            subprocess.run(concat_cmd)
            print(f"🎉 Final Exported: {output_final}")
        else:
            print("No scenes rendered.")

        for tf in temp_files:
            if os.path.exists(tf): os.remove(tf)
        if os.path.exists(concat_list_path): os.remove(concat_list_path)

if __name__ == "__main__":
    main()
