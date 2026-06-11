import os
import subprocess
import shutil

AUDIO_DIR = r"c:\Users\tuesv\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\assets_audio"
EXPORT_DIR = r"c:\Users\tuesv\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\exports"
IMG_DIR = r"c:\Users\tuesv\Documents\DMDG_UT\YOUTUBE\Projects\Subway_Shorts\assets_image"

os.makedirs(EXPORT_DIR, exist_ok=True)

# Scene Images
IMG_HOOK = os.path.join(IMG_DIR, "rainy_subway_hook.png")
IMG_SCENE1 = os.path.join(IMG_DIR, "rainy_subway_heo.png")

# Use dummy audio files from existing assets for the pipeline to run
AUDIO_DUMMY_HOOK = os.path.join(AUDIO_DIR, "001_subway_scene1_KOR.mp3")
AUDIO_DUMMY_SCENE1 = os.path.join(AUDIO_DIR, "002_subway_scene2_KOR.mp3")

languages = ["KOR"]

scenes = {
    "KOR": [
        {"audio": AUDIO_DUMMY_HOOK, "images": [IMG_HOOK], "text": "비 오는 날 지하철 지옥철 타보면 바닥에 온통 빗물이 흥건하잖아.\n꿉꿉한 습기에 이기적인 사람들까지 섞이면 진짜 전쟁터가 따로 없지."},
        {"audio": AUDIO_DUMMY_SCENE1, "images": [IMG_SCENE1], "text": "거기다 한의사 허용준처럼 개량한복 곱게 차려입고는,\n겨드랑이에 젖은 장우산을 가로로 껴서 뒷사람 다리를 찌르는 빌런들이 꼭 있어."},
    ]
}

def get_audio_duration(audio_path):
    ffprobe_exe = r"c:\Users\tuesv\Documents\DMDG_UT\YOUTUBE\ffprobe.exe"
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
    ffmpeg_exe = r"c:\Users\tuesv\Documents\DMDG_UT\YOUTUBE\ffmpeg.exe"
    frames = max(int(duration * 30), 1)
    
    filter_complex = (
        f"[0:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
        f"zoompan=z='min(zoom+0.0008,1.2)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s=1080x1920:fps=30[outv]"
    )
        
    cmd = [
        ffmpeg_exe, "-y", "-loop", "1", "-i", image_path,
        "-t", f"{duration:.3f}",
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_scene_video(image_paths, audio_path, ass_path, output_path):
    print(f"Rendering {os.path.basename(output_path)}...")
    duration = get_audio_duration(audio_path)
    
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
        
    ffmpeg_exe = r"c:\Users\tuesv\Documents\DMDG_UT\YOUTUBE\ffmpeg.exe"
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
    
    rel_ass_path = os.path.basename(ass_path)
    rel_output_path = os.path.basename(output_path)
    
    merge_cmd = [
        ffmpeg_exe, "-y", "-i", temp_visual, "-i", audio_path,
        "-vf", f"subtitles='{rel_ass_path}'",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", rel_output_path
    ]
    subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    if os.path.exists(temp_visual): os.remove(temp_visual)
    os.chdir(orig_cwd)

def main():
    concat_list_path = os.path.join(EXPORT_DIR, "shorts_concat_rainy.txt")
    ffmpeg_exe = r"c:\Users\tuesv\Documents\DMDG_UT\YOUTUBE\ffmpeg.exe"

    for lang in languages:
        print(f"\n--- Starting Rainy Subway Shorts ({lang}) ---")
        output_final = os.path.join(EXPORT_DIR, f"rainy_subway_shorts_1B_{lang}_final.mp4")
        temp_files = []
        
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for i, scene in enumerate(scenes[lang]):
                scene_num = i + 1
                audio_path = scene["audio"]
                temp_vid = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.mp4")
                
                img_paths = scene["images"]
                temp_ass = os.path.join(EXPORT_DIR, f"temp_shorts_scene{scene_num}_{lang}.ass")
                
                temp_files.extend([temp_vid, temp_ass])
                create_ass(temp_ass, scene["text"])
                create_scene_video(img_paths, audio_path, temp_ass, temp_vid)
                
                f.write(f"file '{temp_vid.replace(chr(92), '/')}'\n")

        print("Merging scenes into final Shorts...")
        concat_cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_final]
        subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for tf in temp_files:
            if os.path.exists(tf): os.remove(tf)
        if os.path.exists(concat_list_path): os.remove(concat_list_path)
            
        print(f"[SUCCESS] Exported Final Video: {output_final}")

if __name__ == "__main__":
    main()
