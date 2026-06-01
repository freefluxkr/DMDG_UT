import os
import subprocess

IMG_DIR = r"d:\DMDG_UT\YOUTUBE\result\webtoon"
AUDIO_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\longform"
EXPORT_DIR = r"d:\DMDG_UT\YOUTUBE\result\video_exports"

languages = ["ENG", "JPN"]

texts = {
    "KOR": [
        "1895년의 가을밤, 건청궁의 공기는 유난히 차가웠습니다.\n한 나라의 국모가 머무는 곳이었지만,\n그 밤의 정적은 다가올 비극을 예견하듯 무겁게 가라앉아 있었습니다.",
        "누구도 상상하지 못한 폭력이\n가장 깊은 궁궐의 문을 부수고 들어왔습니다.\n바닥에 떨어진 옥비녀 위로, 붉은 눈물이 번져갔습니다.",
        "그녀가 스러져간 그 자리에, 지금 우리는 서 있습니다.\n부당하게 빼앗긴 삶에 대한 슬픔은 국경을 넘어 우리의 마음을 울립니다.\n이것이 바로 우리가 나누어야 할 슬픔, '한(恨)'입니다.",
        "아픈 역사를 기억하는 가장 따뜻한 방법은,\n서로의 목소리로 그 슬픔을 안아주는 것입니다.\n누군가의 상처가 당신의 목소리로 치유될 수 있도록.\n지금, 당신의 목소리로 다음 글을 읽어주세요."
    ],
    "ENG": [
        "On an autumn night in 1895, the air around Geoncheonggung Palace was unusually cold.\nThough it was the residence of the nation's mother,\nthe silence of that night hung heavy, as if foreseeing the tragedy to come.",
        "Unimaginable violence shattered the doors of the deepest palace.\nUnder the guise of power and ambition, a human being's dignity was ruthlessly trampled.\nOver the jade hairpin fallen on the floor, red tears began to spread.",
        "In the very place where she fell, we stand today.\nThough our languages differ and our worlds are worlds apart,\nthe sorrow for a life unjustly taken resonates across borders, touching our hearts.\nThis is the shared sorrow we must embrace, the essence of Han.",
        "The warmest way to remember a painful history\nis to embrace that sorrow with each other's voices.\nSo that someone's wound might be healed by your voice.\nNow, please read the next line with your voice."
    ],
    "JPN": [
        "1895年の秋の夜、乾清宮の空気はひときわ冷たく感じられました。\n一国の国母が留まる場所でありながら、\nその夜の静寂はやがて訪れる悲劇を予見するかのように重く沈んでいました。",
        "誰も想像すらできなかった暴力が、最も奥深い宮殿の扉を打ち破って入り込みました。\n権力と野望という名の下に、一人の人間の尊厳が無惨にも踏みにじられました。\n床に落ちた玉の簪の上に、赤い涙が滲んでいきました。",
        "彼女が倒れたその場所に、今私たちは立っています。\n言葉が違い、生きてきた世界が違っても、不当に奪われた命への悲しみは国境を越えて私たちの心を打ちます。\nこれこそが、私たちが分かち合うべき悲しみ、ハンなのです。",
        "痛ましい歴史を記憶する最も温かい方法は、\nお互いの声でその悲しみを抱きしめることです。\n誰かの傷が、あなたの声によって癒やされるように。\n今、あなたの声で次の文章を読んでください。"
    ]
}

def create_srt(srt_path, text):
    srt_content = f"1\n00:00:00,000 --> 01:00:00,000\n{text}\n"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

def create_scene_video(image_path, audio_path, srt_path, output_path):
    print(f"Rendering {os.path.basename(output_path)}...")
    safe_srt_path = srt_path.replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", image_path, "-i", audio_path,
        "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_scrolling_scene(audio_path, text, temp_txt_path, output_path):
    print(f"Rendering SCROLLING SCENE {os.path.basename(output_path)}...")
    with open(temp_txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    safe_txt_path = temp_txt_path.replace("\\", "/").replace(":", "\\\\:")
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1920x1080:r=30", "-i", audio_path,
        "-vf", f"drawtext=fontfile='C\\:\\\\Windows\\\\Fonts\\\\malgun.ttf':textfile='{safe_txt_path}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-t*120:line_spacing=30:alpha='if(lt(t,1),0,if(lt(t,2),t-1,1))'",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    concat_list_path = os.path.join(EXPORT_DIR, "concat.txt")

    for lang in languages:
        print(f"\n--- Starting {lang} version ---")
        output_final = os.path.join(EXPORT_DIR, f"longform_{lang}_preview_no_subs.mp4")
        temp_files = []
        
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for scene_num in range(1, 5):
                audio_idx = (scene_num - 1) * 3 + 1
                if lang == "ENG": audio_idx += 1
                if lang == "JPN": audio_idx += 2
                
                audio_path = os.path.join(AUDIO_DIR, f"{audio_idx:03d}_long_scene{scene_num}_{lang}.mp3")
                temp_vid = os.path.join(EXPORT_DIR, f"temp_scene{scene_num}_{lang}.mp4")
                
                if not os.path.exists(audio_path): continue
                
                if scene_num <= 3:
                    image_path = os.path.join(IMG_DIR, f"00{scene_num}_scene{scene_num}.png")
                    temp_srt = os.path.join(EXPORT_DIR, f"temp_scene{scene_num}_{lang}.srt")
                    if not os.path.exists(image_path): continue
                    
                    temp_files.extend([temp_vid, temp_srt])
                    create_srt(temp_srt, texts[lang][scene_num-1])
                    create_scene_video(image_path, audio_path, temp_srt, temp_vid)
                else:
                    # Scene 4 Scrolling
                    temp_txt = os.path.join(EXPORT_DIR, f"temp_scene{scene_num}_{lang}.txt")
                    temp_files.extend([temp_vid, temp_txt])
                    create_scrolling_scene(audio_path, texts[lang][scene_num-1], temp_txt, temp_vid)
                
                f.write(f"file '{temp_vid.replace(chr(92), '/')}'\n")

        print(f"Merging {lang} version...")
        concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_final]
        subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for tf in temp_files:
            if os.path.exists(tf): os.remove(tf)
        if os.path.exists(concat_list_path): os.remove(concat_list_path)
            
        print(f"Exported: {output_final}")

if __name__ == "__main__":
    main()
