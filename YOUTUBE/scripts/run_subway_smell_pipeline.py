import os
import shutil
import asyncio
import subprocess
import edge_tts

# 1. 설정 및 경로 지정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
PROJECT_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Subway_Smell")
IMAGE_DIR = os.path.join(PROJECT_DIR, "assets_image")
AUDIO_DIR = os.path.join(PROJECT_DIR, "assets_audio")
EXPORT_DIR = os.path.join(PROJECT_DIR, "exports")

FFMPEG_EXE = os.path.join(YOUTUBE_DIR, "ffmpeg.exe")
FFPROBE_EXE = os.path.join(YOUTUBE_DIR, "ffprobe.exe")

# 폴더 생성
os.makedirs(EXPORT_DIR, exist_ok=True)

# 3개국어 리스트 및 목소리 설정
languages = ["KOR", "ENG", "JPN"]
voice_settings = {
    "KOR": "ko-KR-InJoonNeural",
    "ENG": "en-US-BrianNeural",
    "JPN": "ja-JP-KeitaNeural"
}

# 대본 정의 (3개국어 번역 포함)
scripts_data = {
    "KOR": [
        {"audio": "001_subway_scene1_KOR.mp3", "text": "지하철 문이 열리는 순간 시작되는 소리 없는 전쟁.\n바로 옆 사람의 냄새입니다."},
        {"audio": "002_subway_scene2_KOR.mp3", "text": "레딧과 SNS를 뜨겁게 달군 3대 냄새 빌런!\n한여름 땀 찌든 내, 덜 마른 옷의 퀴퀴한 쉰내,\n그리고 좁은 밀폐 공간을 마비시키는 독한 향수 폭탄까지."},
        {"audio": "003_subway_scene3_KOR.mp3", "text": "예방법은 간단합니다.\n쉰내 나는 옷은 섬유유연제로 덮지 말고,\n베이킹소다나 온수 세탁으로 균을 확실히 잡으세요.\n향수는 탑승 30분 전에 가볍게만 뿌려주세요."},
        {"audio": "004_subway_scene4_KOR.mp3", "text": "피할 수 없다면 방어하세요!\n코밑에 민트나 레몬 향 멀티밤을 살짝 바르거나,\n휴대용 마스크를 착용하는 것만으로도\n나만의 쾌적한 방어막을 구축할 수 있습니다."},
        {"audio": "005_subway_outro_KOR.mp3", "text": "나를 향한 관리와 타인을 향한 배려로\n더욱 향기로운 하루를 만들어보세요.\n구독하고 더 많은 일상 매너 팁을 만나보세요!"}
    ],
    "ENG": [
        {"audio": "001_subway_scene1_ENG.mp3", "text": "The silent war that begins the moment the subway doors open.\nThe smell of the person right next to you."},
        {"audio": "002_subway_scene2_ENG.mp3", "text": "Three major odor villains that set Reddit and social media ablaze!\nMidsummer sweat, the musty smell of damp laundry,\nand overpowering perfume bombs that paralyze confined spaces."},
        {"audio": "003_subway_scene3_ENG.mp3", "text": "Prevention is simple.\nDon't mask sour clothes with fabric softener;\nsanitize them with baking soda or warm water.\nSpray perfume lightly 30 minutes before boarding."},
        {"audio": "004_subway_scene4_ENG.mp3", "text": "If you can't avoid it, defend yourself!\nSimply dab a bit of mint or lemon balm under your nose,\nor wear a mask to build your own fresh shield."},
        {"audio": "005_subway_outro_ENG.mp3", "text": "Create a more fragrant day through self-care and consideration.\nSubscribe for more daily etiquette tips!"}
    ],
    "JPN": [
        {"audio": "001_subway_scene1_JPN.mp3", "text": "地下鉄の扉が開いた瞬間から始まる、音のない戦争。\nそれは、すぐ隣의 人의 『臭い』입니다."},
        {"audio": "002_subway_scene2_JPN.mp3", "text": "ネットで話題의 3大悪臭モンスター！\n真夏の汗の臭い、生乾きの服のツーンとする臭い、\nそして狭い密閉空間を麻痺させる強烈な香水テロまで."},
        {"audio": "003_subway_scene3_JPN.mp3", "text": "予防策は簡単です.\n生乾きの服は柔軟剤でごまかさず、\n重曹や温水洗濯で菌をしっかり除菌しましょう.\n香水は乗車30分前に軽くつけるのがマナーです."},
        {"audio": "004_subway_scene4_JPN.mp3", "text": "避けられないなら防衛しましょう!\n鼻の下にミントやレモンのバームを少し塗るか、\nマスクをつけるだけで、自分だけの快適な防御壁を作れます."},
        {"audio": "005_subway_outro_JPN.mp3", "text": "自分へのケアと他人への思いやりで、\nより快適な一日を作りましょう.\nチャンネル登録して、日々のマナー情報をチェック!"}
    ]
}

# 씬에 들어갈 공통 이미지 세트 정의
scene_images = [
    ["subway_smell_scene1.png"],                                                   # 씬 1
    ["subway_smell_scene2_sweat.png", "subway_smell_scene2_damp.png", "subway_smell_scene2_perfume.png"], # 씬 2 (빌런 3종)
    ["subway_smell_scene3.png"],                                                   # 씬 3
    ["subway_smell_scene4.png"],                                                   # 씬 4
    ["subway_smell_scene5.png"]                                                    # 씬 5
]

# 1. 루트 폴더 정리 함수
async def clean_root_dir():
    print("\n--- 1. 루트 폴더 정리 작업 ---")
    files_to_delete = [
        os.path.join(BASE_DIR, "이미지_복사.bat"),
        os.path.join(BASE_DIR, "오디오_생성.bat"),
        os.path.join(BASE_DIR, "copy_subway_images.py")
    ]
    for file_path in files_to_delete:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"[삭제 완료] {os.path.basename(file_path)}")
            except Exception as e:
                print(f"[삭제 실패] {os.path.basename(file_path)}: {e}")

# 2. 3개국어 오디오 파일 생성 (TTS)
async def generate_tts():
    print("\n--- 2. 3개국어 오디오(TTS) 생성 작업 ---")
    os.makedirs(AUDIO_DIR, exist_ok=True)
    for lang in languages:
        print(f"\n[{lang} 버전 음성 생성 중...]")
        for idx, item in enumerate(scripts_data[lang]):
            audio_path = os.path.join(AUDIO_DIR, item["audio"])
            if os.path.exists(audio_path):
                print(f"[스킵] 오디오 파일이 이미 존재합니다: {item['audio']}")
                continue
                
            print(f"생성 중: {item['audio']} ...")
            rate = "-5%"
            pitch = "-5Hz"
            try:
                communicate = edge_tts.Communicate(item["text"], voice_settings[lang], rate=rate, pitch=pitch)
                await communicate.save(audio_path)
                print(f"[저장 완료] {audio_path}")
            except Exception as e:
                print(f"[생성 실패] {audio_path}: {e}")

# 3. 비디오 렌더링 헬퍼 함수들
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
PlayResX: 1080
PlayResY: 1920
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,62,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,0,2,80,80,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,1:00:00.00,Default,,0,0,0,,{ass_text}
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

def create_image_video(image_path, duration, output_path):
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
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_scene(image_files, audio_path, ass_path, output_path):
    duration = get_audio_duration(audio_path)
    
    orig_cwd = os.getcwd()
    os.chdir(EXPORT_DIR)
    
    segment_paths = []
    n = len(image_files)
    seg_duration = duration / n
    
    for idx, img_name in enumerate(image_files):
        img_path = os.path.join(IMAGE_DIR, img_name)
        current_dur = seg_duration if idx < n - 1 else (duration - seg_duration * idx)
        seg_vid_path = f"temp_seg_{idx}.mp4"
        create_image_video(img_path, current_dur, seg_vid_path)
        segment_paths.append(seg_vid_path)
        
    temp_visual = "temp_visual.mp4"
    concat_txt_path = "temp_concat.txt"
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for seg in segment_paths:
            f.write(f"file '{seg}'\n")
            
    concat_cmd = [FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_path, "-c", "copy", temp_visual]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for seg in segment_paths:
        if os.path.exists(seg): os.remove(seg)
    if os.path.exists(concat_txt_path): os.remove(concat_txt_path)
    
    rel_ass_path = os.path.basename(ass_path)
    rel_output_path = os.path.basename(output_path)
    
    merge_cmd = [
        FFMPEG_EXE, "-y", "-i", temp_visual, "-i", audio_path,
        "-vf", f"subtitles='{rel_ass_path}'",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", rel_output_path
    ]
    subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(temp_visual): os.remove(temp_visual)
    os.chdir(orig_cwd)

# 4. 3개국어 비디오 렌더링 및 최종 병합
def render_full_videos():
    print("\n--- 3. 3개국어 비디오 렌더링 및 자막/애니메이션 작업 ---")
    
    for lang in languages:
        print(f"\n=========================================")
        print(f"Rendering {lang} Shorts Version")
        print(f"=========================================")
        
        output_final = os.path.join(EXPORT_DIR, f"subway_smell_shorts_{lang}_final.mp4")
        concat_list_path = os.path.join(EXPORT_DIR, f"shorts_concat_{lang}.txt")
        temp_files = []
        
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for idx, scene in enumerate(scripts_data[lang]):
                scene_num = idx + 1
                audio_path = os.path.join(AUDIO_DIR, scene["audio"])
                images = scene_images[idx]
                
                # 이미지 존재 여부 확인
                missing_img = False
                for img in images:
                    if not os.path.exists(os.path.join(IMAGE_DIR, img)):
                        print(f"[에러] 이미지가 누락되었습니다: {img}")
                        missing_img = True
                if missing_img or not os.path.exists(audio_path):
                    continue
                    
                temp_vid = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.mp4")
                temp_ass = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.ass")
                
                temp_files.extend([temp_vid, temp_ass])
                
                # 자막(ASS) 생성
                create_ass(temp_ass, scene["text"])
                
                # 씬 렌더링
                print(f"[{lang}] 씬 {scene_num} 렌더링 중...")
                render_scene(images, audio_path, temp_ass, temp_vid)
                
                f.write(f"file '{temp_vid.replace(chr(92), '/')}'\n")
                
        if len(temp_files) > 0:
            print(f"\n[{lang}] 최종 비디오 병합 중...")
            concat_cmd = [FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_final]
            res = subprocess.run(concat_cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"[성공] 최종 {lang} 쇼츠 영상이 생성되었습니다: {output_final}")
            else:
                print(f"[실패] 최종 병합 오류 ({lang}):\n{res.stderr}")
                
        # 임시 작업 파일 정리
        for tf in temp_files:
            if os.path.exists(tf): os.remove(tf)
        if os.path.exists(concat_list_path): os.remove(concat_list_path)

async def main():
    print("========================================================")
    print("     지하철 냄새 쇼츠 통합 렌더링 파이프라인 (3개국어 지원)")
    print("========================================================")
    
    # 1. 루트 폴더 정리
    await clean_root_dir()
    
    # 2. 오디오(TTS) 생성 및 검증
    await generate_tts()
    
    # 3. 비디오 애니메이션/자막 인코딩 및 최종 병합
    render_full_videos()
    
    print("\n========================================================")
    print("     모든 3개국어 영상 제작 프로세스가 완료되었습니다!")
    print("========================================================")

if __name__ == "__main__":
    asyncio.run(main())
