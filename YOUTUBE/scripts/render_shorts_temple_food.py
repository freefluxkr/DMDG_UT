import os
import subprocess

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
FFMPEG_EXE = os.path.join(YOUTUBE_DIR, "ffmpeg.exe")
FFPROBE_EXE = os.path.join(YOUTUBE_DIR, "ffprobe.exe")

# Define projects config
PROJECTS = {
    "hermitage": {
        "name": "TempleFood",
        "audio_dir": os.path.join(YOUTUBE_DIR, r"Projects\TempleFood\assets_audio"),
        "img_dir": os.path.join(YOUTUBE_DIR, r"Projects\TempleFood\assets_image"),
        "video_dir": os.path.join(YOUTUBE_DIR, r"Projects\TempleFood\assets_video"),
        "export_dir": os.path.join(YOUTUBE_DIR, r"Projects\TempleFood\exports"),
        "scenes": {
            "KOR": [
                {"audio": "scene1_KOR.mp3", "image": "scene1.png", "text": "지리산 깊은 암자의 부엌.\n자연이 계절에 맞춰 내어준 정직한 재료들이 놓입니다.\n나를 낮추고 세상과 연결되는 고요한 시간입니다."},
                {"audio": "scene2_KOR.mp3", "image": "scene2.png", "text": "뜨거운 가마솥 안에서 취나물의 쓴맛은 향긋함으로 변하고,\n들기름으로 고소함을 더합니다.\n세상을 향한 날 선 마음들을 데쳐내어 다스리는 시간입니다."},
                {"audio": "scene3_KOR.mp3", "image": "scene3.png", "text": "두툼한 표고버섯에 달콤한 조청과 간장이 깊이 배어듭니다.\n고기 한 점, 마늘 한 톨 없이도,\n버섯이 가진 대지의 풍미가 거친 무사의 식탁을 채웁니다."},
                {"audio": "scene4_KOR.mp3", "image": "scene4.png", "text": "달큰한 단호박과 옹심이가 들깨의 품에서 걸쭉하게 끓어오릅니다.\n비우고 채워내는 산사의 따뜻한 온기가\n서씨의 깊은 상처를 어루만집니다."},
                {"audio": "scene5_KOR.mp3", "image": "scene5.png", "text": "오늘 하루, 복잡한 세상의 짐을 내려놓고\n마음을 비워내는 사찰 요리 어떠신가요?\n평온한 산사로 당신을 초대합니다."}
            ],
            "ENG": [
                {"audio": "scene1_ENG.mp3", "image": "scene1.png", "text": "A kitchen in a deep mountain hermitage.\nHonest ingredients, given in accordance with the seasons, are laid out.\nA quiet time to lower oneself and connect with the world."},
                {"audio": "scene2_ENG.mp3", "image": "scene2.png", "text": "Inside the hot cast-iron pot, the bitterness of Chwinamul turns into fragrance,\nenriched by savory perilla oil.\nIt is a time to blanch away their sharp edges towards the world."},
                {"audio": "scene3_ENG.mp3", "image": "scene3.png", "text": "Sweet rice syrup and soy sauce seep deeply into the chewy shiitake mushrooms.\nWithout a single piece of meat or clove of garlic,\nthe earthy flavor of the mushrooms fills the weary hunter's table."},
                {"audio": "scene4_ENG.mp3", "image": "scene4.png", "text": "Sweet pumpkin and dough balls boil in the savory embrace of perilla seeds.\nThe warm comfort of the temple, of emptying and filling,\ngently caresses Seo-ssi's deep scars."},
                {"audio": "scene5_ENG.mp3", "image": "scene5.png", "text": "How about a temple dish to lightly empty your mind today?\nWe invite you to this peaceful mountain temple."}
            ]
        }
    },
    "us_kitchen": {
        "name": "TempleFoodUS",
        "audio_dir": os.path.join(YOUTUBE_DIR, r"Projects\TempleFoodUS\assets_audio"),
        "img_dir": os.path.join(YOUTUBE_DIR, r"Projects\TempleFoodUS\assets_image"),
        "video_dir": os.path.join(YOUTUBE_DIR, r"Projects\TempleFoodUS\assets_video"),
        "export_dir": os.path.join(YOUTUBE_DIR, r"Projects\TempleFoodUS\exports"),
        "scenes": {
            "KOR": [
                {"audio": "scene1_KOR.mp3", "image": "scene1.png", "text": "지친 일상을 정화하는 더피의 소소 밥상.\n오늘은 미국의 마트에서 맑은 공양을 위한 장보기가 시작됩니다."},
                {"audio": "scene2_KOR.mp3", "image": "scene2.png", "text": "한국의 전통 산나물 대신, 미국 마트의 싱싱한 케일과 버터넛 스쿼시가\n서씨와 더피의 솜씨로 맑은 사찰음식이 됩니다."},
                {"audio": "scene3_KOR.mp3", "image": "scene3.png", "text": "케일은 흐르는 물에 씻어 억센 줄기를 도려내고 부드러운 잎사귀만 남깁니다.\n손길 끝에 정성을 다하는 시간입니다."},
                {"audio": "scene4_KOR.mp3", "image": "scene4.png", "text": "마늘과 파를 완전히 빼낸 빈자리에 생강과 들기름의 깊은 맛이 스며들도록,\n작은 채소들을 정성껏 다듬어 나갑니다."},
                {"audio": "scene5_KOR.mp3", "image": "scene5.png", "text": "두꺼운 껍질 속 드러난 단호박의 노란 속살을 먹기 좋은 크기로 썰어냅니다.\n버려지는 것 없이 재료의 본질을 살립니다."},
                {"audio": "scene6_KOR.mp3", "image": "scene6.png", "text": "뜨거운 김 속에서 끓어오르는 맑은 온기.\n고기 한 점 없이도 스쿼시의 단맛과 들깨의 걸쭉함이 주방을 가득 채웁니다."},
                {"audio": "scene7_KOR.mp3", "image": "scene7.png", "text": "이방인 친구 바비와 한의사 허용준 원장이 함께 마주 앉은 식탁.\n낯선 이국 땅에서 소박한 자연의 밥상이 그들을 위로합니다."},
                {"audio": "scene8_KOR.mp3", "image": "scene8.png", "text": "오늘 저녁은 당신의 주방에 오신채 없는 평온한 밥상을 올려보는 건 어떨까요?\n더피의 소소 밥상 완성."}
            ],
            "ENG": [
                {"audio": "scene1_ENG.mp3", "image": "scene1.png", "text": "Duffy's Soso Table to purify your weary days.\nToday, a grocery shopping journey for a pure temple meal begins in an American store."},
                {"audio": "scene2_ENG.mp3", "image": "scene2.png", "text": "Instead of traditional wild herbs, fresh kale and butternut squash from a US store\nwill become pure temple food in the hands of Seo-ssi and Duffy."},
                {"audio": "scene3_ENG.mp3", "image": "scene3.png", "text": "Clean the kale under running water, trim away the tough stems, and keep only the tender leaves.\nA time of dedication at their fingertips."},
                {"audio": "scene4_ENG.mp3", "image": "scene4.png", "text": "Leaving out all garlic and onions, they carefully prep the small vegetables\nto absorb the deep aromas of ginger and perilla oil."},
                {"audio": "scene5_ENG.mp3", "image": "scene5.png", "text": "Peeling away the tough skin to reveal the golden flesh, slicing it into bite-sized pieces.\nPreserving the essence without wasting a thing."},
                {"audio": "scene6_ENG.mp3", "image": "scene6.png", "text": "A pure warmth boiling inside the gentle steam.\nEven without a single piece of meat, the sweetness of squash and richness of perilla seed fills the kitchen."},
                {"audio": "scene7_ENG.mp3", "image": "scene7.png", "text": "A table shared with their foreign friend Bobby and Korean doctor Heo Yong-joon.\nIn this unfamiliar land, a simple table of nature comforts them."},
                {"audio": "scene8_ENG.mp3", "image": "scene8.png", "text": "Tonight, why not set a peaceful, allium-free table in your kitchen?\nDuffy's Soso Table is served."}
            ]
        }
    }
}

languages = ["KOR", "ENG"]

def get_audio_duration(audio_path):
    cmd = [
        FFPROBE_EXE, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        return float(res.stdout.strip())
    return 5.0

def create_ass(ass_path, text):
    ass_text = text.replace('\n', '\\N')
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,55,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,0,2,80,80,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,1:00:00.00,Default,,0,0,0,,{ass_text}
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

def create_image_video(image_path, duration, output_path):
    # Widescreen Ken burns zoom-in
    frames = max(int(duration * 30), 1)
    filter_complex = (
        f"[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
        f"zoompan=z='min(zoom+0.0008,1.2)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s=1920x1080:fps=30[outv]"
    )
    cmd = [
        FFMPEG_EXE, "-y", "-loop", "1", "-i", image_path,
        "-t", f"{duration:.3f}",
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_scene(image_path, video_path, audio_path, ass_path, export_dir, output_path, is_widescreen=False):
    duration = get_audio_duration(audio_path)
    
    orig_cwd = os.getcwd()
    os.chdir(export_dir)
    
    temp_visual = "temp_visual.mp4"
    if video_path and os.path.exists(video_path):
        print(f"Using motion video: {video_path}")
        scale_val = "1920:1080" if is_widescreen else "1080:1920"
        cmd = [
            FFMPEG_EXE, "-y",
            "-stream_loop", "-1",
            "-i", video_path,
            "-t", f"{duration:.3f}",
            "-vf", f"scale={scale_val}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            temp_visual
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(f"Fallback to static image: {image_path}")
        if is_widescreen:
            create_image_video(image_path, duration, temp_visual)
        else:
            # Fallback to vertical static
            frames = max(int(duration * 30), 1)
            filter_complex = (
                f"[0:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
                f"zoompan=z='min(zoom+0.0008,1.2)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s=1080x1920:fps=30[outv]"
            )
            cmd = [
                FFMPEG_EXE, "-y", "-loop", "1", "-i", image_path,
                "-t", f"{duration:.3f}",
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", temp_visual
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    rel_ass_path = os.path.basename(ass_path)
    rel_output_path = os.path.basename(output_path)
    
    merge_cmd = [
        FFMPEG_EXE, "-y", "-i", temp_visual, "-i", audio_path,
        "-vf", f"subtitles='{rel_ass_path}'",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", rel_output_path
    ]
    res = subprocess.run(merge_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg error merging subtitles/audio:\n{res.stderr}")
        
    if os.path.exists(temp_visual): os.remove(temp_visual)
    os.chdir(orig_cwd)

def main():
    print("=== STARTING TEMPLE FOOD SHORTS RENDERING PIPELINE (FFMPEG) ===")
    
    # 1. Render normal projects (hermitage [vertical] and us_kitchen [widescreen 16:9])
    for proj_id, config in PROJECTS.items():
        print(f"\n=========================================")
        print(f"Rendering Project: {config['name']}")
        print(f"=========================================")
        
        os.makedirs(config["export_dir"], exist_ok=True)
        concat_list_path = os.path.join(config["export_dir"], "shorts_concat.txt")
        
        is_widescreen = (proj_id == "us_kitchen")
        
        for lang in languages:
            print(f"\n--- Starting {lang} version ---")
            output_final = os.path.join(config["export_dir"], f"temple_food_{proj_id}_{lang}_final.mp4")
            temp_files = []
            
            with open(concat_list_path, "w", encoding="utf-8") as f:
                for idx, scene in enumerate(config["scenes"][lang]):
                    scene_num = idx + 1
                    audio_path = os.path.join(config["audio_dir"], scene["audio"])
                    image_path = os.path.join(config["img_dir"], scene["image"])
                    video_path = os.path.join(config["video_dir"], scene["image"].replace(".png", "_motion.mp4"))
                    temp_vid = os.path.join(config["export_dir"], f"temp_shorts_scene{scene_num}_{lang}.mp4")
                    temp_ass = os.path.join(config["export_dir"], f"temp_shorts_scene{scene_num}_{lang}.ass")
                    
                    if not os.path.exists(audio_path):
                        print(f"Missing audio: {audio_path}")
                        continue
                    if not os.path.exists(image_path):
                        print(f"Missing image: {image_path}")
                        continue
                        
                    temp_files.extend([temp_vid, temp_ass])
                    create_ass(temp_ass, scene["text"])
                    render_scene(image_path, video_path, audio_path, temp_ass, config["export_dir"], temp_vid, is_widescreen=is_widescreen)
                    
                    f.write(f"file '{temp_vid.replace(chr(92), '/')}'\n")
            
            if len(temp_files) > 0:
                print(f"Merging {lang} final video...")
                concat_cmd = [FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_final]
                res = subprocess.run(concat_cmd, capture_output=True, text=True)
                if res.returncode != 0:
                    print(f"FFmpeg merge error:\n{res.stderr}")
                else:
                    print(f"Exported Shorts video: {output_final}")
            
            for tf in temp_files:
                if os.path.exists(tf): os.remove(tf)
            if os.path.exists(concat_list_path): os.remove(concat_list_path)

    # 2. Build Unified Special video is disabled/skipped here since Hermitage (9:16) and US (16:9) have different aspect ratios.
    print("\n=== RENDERING PIPELINE COMPLETED ===")

if __name__ == "__main__":
    main()
