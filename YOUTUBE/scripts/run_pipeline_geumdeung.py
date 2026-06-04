import asyncio
import edge_tts
import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
AUDIO_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Geumdeungjisa\assets_audio")
IMG_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Geumdeungjisa\assets_image")
EXPORT_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Geumdeungjisa\exports")
FFMPEG_EXE = os.path.join(YOUTUBE_DIR, "ffmpeg.exe")
FFPROBE_EXE = os.path.join(YOUTUBE_DIR, "ffprobe.exe")
SCRIPT_JSON_PATH = os.path.join(YOUTUBE_DIR, r"narration\002_geumdeungjisa_shorts_v2_script.json")
VIDEO_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Geumdeungjisa\assets_video")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# Voice profiles
VOICE_MAP = {
    1: {"voice": "ko-KR-InJoonNeural", "rate": "+2%", "pitch": "-2Hz"},   # Jeongjo (Strong, youthful tone)
    2: {"voice": "ko-KR-InJoonNeural", "rate": "-15%", "pitch": "-12Hz"}, # Yeongjo (Tragic, elder tone - slower, lower pitch)
    3: {"voice": "ko-KR-InJoonNeural", "rate": "-12%", "pitch": "-10Hz"}, # Yeongjo (Old, sorrowful tone)
    4: {
        "shin": {"voice": "ko-KR-InJoonNeural", "rate": "+3%", "pitch": "+6Hz"}, # Shinhyup (Trembling official - styled higher/faster)
        "jeongjo": {"voice": "ko-KR-InJoonNeural", "rate": "+5%", "pitch": "-1Hz"} # Jeongjo furious
    },
    5: {"voice": "ko-KR-InJoonNeural", "rate": "-2%", "pitch": "-4Hz"}   # Haru (Narration)
}

# Image file paths for scenes
SCENE_IMAGES = {
    1: os.path.join(IMG_DIR, "geumdeung_shorts_box.png"),
    2: os.path.join(IMG_DIR, "geumdeung_shorts_sad.png"),
    3: os.path.join(IMG_DIR, "geumdeung_shorts_write.png"),
    4: os.path.join(IMG_DIR, "geumdeung_shorts_jeongjo.png"),
    5: os.path.join(IMG_DIR, "geumdeung_shorts_box.png")
}

# Search patterns for SFX files in workspace
SFX_PATTERNS = {
    1: "lightning", # thunder/lightning
    2: "wood",      # thud/hit/crash
    3: "paper",     # paper rustle/brush
    4: "sword",     # sword draw/ring
    5: "clock"      # clock tick
}

def find_sfx_file(pattern):
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if pattern.lower() in file.lower() and file.endswith(('.wav', '.mp3')):
                path = os.path.join(root, file)
                print(f"Found SFX file for pattern '{pattern}': {path}")
                return path
    return None

def create_foreground_image(image_path, scene_index, output_path):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    # Create soft radial mask
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    cx, cy = width // 2, height // 2
    
    if scene_index == 0: # Box in the middle-top
        rx, ry = int(width * 0.35), int(height * 0.25)
        cy = int(height * 0.4)
    elif scene_index == 1: # King Yeongjo in red Gonryongpo
        rx, ry = int(width * 0.4), int(height * 0.35)
        cy = int(height * 0.5)
    elif scene_index == 2: # King writing (close-up of hand)
        rx, ry = int(width * 0.45), int(height * 0.35)
        cy = int(height * 0.6)
    elif scene_index == 3: # King Jeongjo standing tall
        rx, ry = int(width * 0.38), int(height * 0.40)
        cy = int(height * 0.45)
    else:
        rx, ry = int(width * 0.4), int(height * 0.3)
        
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    
    # Blur mask to create soft alpha edges
    blurred_mask = mask.filter(ImageFilter.GaussianBlur(radius=60))
    img.putalpha(blurred_mask)
    img.save(output_path, "PNG")

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs == 100:
        s += 1
        cs = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_kinetic_ass(ass_path, words_data):
    lines = []
    lines.append("[Script Info]")
    lines.append("ScriptType: v4.00+")
    lines.append("PlayResX: 1080")
    lines.append("PlayResY: 1920")
    lines.append("WrapStyle: 1")
    lines.append("")
    lines.append("[V4+ Styles]")
    lines.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    # Bottom-Center Alignment = 2, MarginV = 400
    lines.append("Style: Default,Malgun Gothic,130,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,12,8,2,0,0,400,1")
    lines.append("")
    lines.append("[Events]")
    lines.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")
    
    for i, w in enumerate(words_data):
        start_str = format_ass_time(w["start"])
        end_str = format_ass_time(w["end"])
        word_text = w["word"]
        
        # Cycle through colors: White, Yellow
        if i % 2 == 0:
            color_tag = "{\\c&H00FFFFFF}" # White
        else:
            color_tag = "{\\c&H0000E5FF}" # Premium Yellow/Gold
            
        # Dramatic pop bounce scale effect
        bounce_tag = "{\\fscx135\\fscy135\\t(0,120,\\fscx100\\fscy100)}"
        lines.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{bounce_tag}{color_tag}{word_text}")
        
    with open(ass_path, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(lines))

async def generate_tts_from_script():
    print(f"Loading script from {SCRIPT_JSON_PATH}...")
    with open(SCRIPT_JSON_PATH, "r", encoding="utf-8") as f:
        script_data = json.load(f)
        
    scene_words = {}
    
    print("Checking/Generating TTS voice files with word boundaries...")
    for scene in script_data:
        num = scene["scene_number"]
        dialogue = scene["dialogue"]
        
        # === SKIP TTS if audio already exists ===
        if num == 4:
            existing_audio = os.path.join(AUDIO_DIR, "004_geumdeung_scene4.mp3")
        else:
            existing_audio = os.path.join(AUDIO_DIR, f"00{num}_geumdeung_scene{num}.mp3")
        
        if os.path.exists(existing_audio):
            print(f"[SKIP] Scene {num} audio exists ({os.path.basename(existing_audio)}). Re-generating to capture word boundaries...")
            # Still need word boundaries for kinetic subtitles — re-generate TTS to memory only
            # (audio file will be overwritten with same content)

        
        if num == 4:
            parts = [p.strip() for p in dialogue.split('/')]
            shin_text = parts[0]
            jeongjo_text = parts[1]
            
            shin_file = os.path.join(AUDIO_DIR, "004_scene4_shin.mp3")
            jeongjo_file = os.path.join(AUDIO_DIR, "004_scene4_jeongjo.mp3")
            
            print(f"Generating Scene 4 dialogue components...")
            # 1. Shinhyup Part
            c1 = edge_tts.Communicate(shin_text, VOICE_MAP[4]["shin"]["voice"], 
                                      rate=VOICE_MAP[4]["shin"]["rate"], pitch=VOICE_MAP[4]["shin"]["pitch"])
            shin_words = []
            with open(shin_file, "wb") as fp:
                async for chunk in c1.stream():
                    if chunk["type"] == "audio":
                        fp.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        shin_words.append({
                            "word": chunk["text"],
                            "start": (chunk["offset"] / 10000) / 1000.0,
                            "end": ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                        })
            
            # 2. Jeongjo Part
            c2 = edge_tts.Communicate(jeongjo_text, VOICE_MAP[4]["jeongjo"]["voice"], 
                                      rate=VOICE_MAP[4]["jeongjo"]["rate"], pitch=VOICE_MAP[4]["jeongjo"]["pitch"])
            jeongjo_words = []
            with open(jeongjo_file, "wb") as fp:
                async for chunk in c2.stream():
                    if chunk["type"] == "audio":
                        fp.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        jeongjo_words.append({
                            "word": chunk["text"],
                            "start": (chunk["offset"] / 10000) / 1000.0,
                            "end": ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                        })
            
            if not shin_words:
                shin_dur = get_audio_duration(shin_file) if os.path.exists(shin_file) else 2.0
                shin_list = [w for w in shin_text.split() if w.strip()]
                w_dur = shin_dur / len(shin_list) if shin_list else 1.0
                shin_words = [{"word": w, "start": i * w_dur, "end": (i+1) * w_dur} for i, w in enumerate(shin_list)]
                
            if not jeongjo_words:
                jeong_dur = get_audio_duration(jeongjo_file) if os.path.exists(jeongjo_file) else 5.0
                jeong_list = [w for w in jeongjo_text.split() if w.strip()]
                w_dur = jeong_dur / len(jeong_list) if jeong_list else 1.0
                jeongjo_words = [{"word": w, "start": i * w_dur, "end": (i+1) * w_dur} for i, w in enumerate(jeong_list)]

            # Mix scene 4 audio and adjust timestamps (Jeongjo delayed by 2.2s = 2200ms)
            delay_ms = 2200
            delay_sec = delay_ms / 1000.0
            
            for w in jeongjo_words:
                w["start"] += delay_sec
                w["end"] += delay_sec
                
            scene_words[4] = {"words": shin_words + jeongjo_words, "dialogue": dialogue}
            
            output_file = os.path.join(AUDIO_DIR, "004_geumdeung_scene4.mp3")
            print("Mixing Scene 4 audio...")
            cmd = [
                FFMPEG_EXE, "-y",
                "-i", shin_file,
                "-i", jeongjo_file,
                "-filter_complex", f"[0:a]adelay=0|0,volume=1.8[a0];[1:a]adelay={delay_ms}|{delay_ms},volume=2.5[a1];[a0][a1]amix=inputs=2:duration=longest:dropout_transition=0[outa]",
                "-map", "[outa]",
                "-c:a", "libmp3lame", "-q:a", "2",
                output_file
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"Successfully mixed Scene 4: {output_file}")
                if os.path.exists(shin_file): os.remove(shin_file)
                if os.path.exists(jeongjo_file): os.remove(jeongjo_file)
            else:
                print(f"Failed to mix dialogue:\n{res.stderr}")
                
        else:
            output_file = os.path.join(AUDIO_DIR, f"00{num}_geumdeung_scene{num}.mp3")
            print(f"Generating Scene {num} TTS...")
            c = edge_tts.Communicate(dialogue, VOICE_MAP[num]["voice"], 
                                     rate=VOICE_MAP[num]["rate"], pitch=VOICE_MAP[num]["pitch"])
            words = []
            with open(output_file, "wb") as fp:
                async for chunk in c.stream():
                    if chunk["type"] == "audio":
                        fp.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        words.append({
                            "word": chunk["text"],
                            "start": (chunk["offset"] / 10000) / 1000.0,
                            "end": ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                        })
            if not words:
                dur = get_audio_duration(output_file) if os.path.exists(output_file) else 5.0
                w_list = [w for w in dialogue.split() if w.strip()]
                w_dur = dur / len(w_list) if w_list else 1.0
                words = [{"word": w, "start": i * w_dur, "end": (i+1) * w_dur} for i, w in enumerate(w_list)]
                
            scene_words[num] = {"words": words, "dialogue": dialogue}
            
    return scene_words

def get_audio_duration(audio_path):
    cmd = [
        FFPROBE_EXE, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        return float(res.stdout.strip())
    return 5.0

def create_scene_video(image_path, foreground_path, duration, output_path, scene_index):
    frames = max(int(duration * 30), 1)
    
    # 1. Background layer: Blur + slow zoom
    bg_filter = (
        f"[0:v]boxblur=25,scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
        f"zoompan=z='min(zoom+0.0004,1.1)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s=1080x1920:fps=30[bg];"
    )
    
    # 2. Foreground layer: Crop + faster zoom + shake
    if scene_index == 1: # Yeongjo crying: Heavy shake
        fg_filter = (
            f"[1:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
            f"zoompan=z='min(zoom+0.0012,1.2)':x='(iw-iw/zoom)/2+18*sin(2*PI*on/30*1.5)':y='(ih-ih/zoom)/2':d={frames}:s=1080x1920:fps=30[fg];"
        )
    elif scene_index == 3: # Jeongjo furious: Shaking zoom
        fg_filter = (
            f"[1:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
            f"zoompan=z='min(zoom+0.0016,1.25)':x='(iw-iw/zoom)/2+12*sin(2*PI*on/10)':y='(ih-ih/zoom)/2':d={frames}:s=1080x1920:fps=30[fg];"
        )
    else: # Normal zoom
        fg_filter = (
            f"[1:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
            f"zoompan=z='min(zoom+0.0010,1.2)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s=1080x1920:fps=30[fg];"
        )
        
    # 3. Combine layers + Vignette for cinematic look
    overlay_filter = (
        f"[bg][fg]overlay=0:0[combined];"
        f"[combined]vignette=PI/4[outv]"
    )
    
    filter_complex = bg_filter + fg_filter + overlay_filter
    
    cmd = [
        FFMPEG_EXE, "-y", 
        "-loop", "1", "-i", image_path,
        "-loop", "1", "-i", foreground_path,
        "-t", f"{duration:.3f}",
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_segments(scene_words):
    print("Rendering video segments with 3D Parallax and Kinetic Subtitles...")
    temp_files = []
    
    orig_cwd = os.getcwd()
    os.chdir(EXPORT_DIR)
    
    concat_list_path = "geumdeung_concat.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for idx in range(5):
            scene_num = idx + 1
            audio_file = f"00{scene_num}_geumdeung_scene{scene_num}.mp3"
            audio_path = os.path.join(AUDIO_DIR, audio_file)
            image_path = SCENE_IMAGES[scene_num]
            
            # Temporary files in current directory (EXPORT_DIR)
            temp_fg = f"temp_fg_{scene_num}.png"
            temp_vid_no_audio = f"temp_scene_{scene_num}_no_audio.mp4"
            temp_ass = f"temp_scene_{scene_num}.ass"
            output_vid = f"scene{scene_num}_final.mp4"
            
            # Create Foreground transparent layer
            create_foreground_image(image_path, idx, temp_fg)
            
            duration = get_audio_duration(audio_path)
            
            words_data = scene_words[scene_num]["words"]
                
            # Generate word-by-word kinetic subtitles
            generate_kinetic_ass(temp_ass, words_data)
            
            # Check if Runway motion video exists
            runway_video_name = f"scene{scene_num}_motion.mp4"
            runway_video_path = os.path.join(VIDEO_DIR, runway_video_name)
            if os.path.exists(runway_video_path):
                print(f"Using Runway motion video for Scene {scene_num}: {runway_video_path}")
                # Loop and scale Runway video to match audio duration
                loop_cmd = [
                    FFMPEG_EXE, "-y",
                    "-stream_loop", "-1",
                    "-i", runway_video_path,
                    "-t", f"{duration:.3f}",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                    temp_vid_no_audio
                ]
                subprocess.run(loop_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                # Create the zoomed 3D parallax visual base video
                create_scene_video(image_path, temp_fg, duration, temp_vid_no_audio, idx)
            
            # Find and Mix SFX if available
            sfx_pattern = SFX_PATTERNS[scene_num]
            sfx_file = find_sfx_file(sfx_pattern)
            
            mixed_audio_file = f"temp_mixed_audio_{scene_num}.mp3"
            if sfx_file:
                # Mix original TTS with SFX
                if scene_num == 4: # Sword clang at Jeongjo start (2.2s)
                    audio_filter = f"[0:a]volume=1.0[a0];[1:a]adelay=2200|2200,volume=1.2[a1];[a0][a1]amix=inputs=2:duration=first[outa]"
                elif scene_num == 1: # Lightning thunder at start (0s)
                    audio_filter = f"[0:a]volume=1.0[a0];[1:a]adelay=0|0,volume=1.5[a1];[a0][a1]amix=inputs=2:duration=first[outa]"
                else: # Generic delay (0s)
                    audio_filter = f"[0:a]volume=1.0[a0];[1:a]adelay=0|0,volume=0.8[a1];[a0][a1]amix=inputs=2:duration=first[outa]"
                    
                mix_cmd = [
                    FFMPEG_EXE, "-y", "-i", audio_path, "-i", sfx_file,
                    "-filter_complex", audio_filter,
                    "-map", "[outa]", "-c:a", "libmp3lame", "-q:a", "2", mixed_audio_file
                ]
                subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                target_audio = mixed_audio_file
                temp_files.append(mixed_audio_file)
            else:
                target_audio = audio_path
            
            # Merge visual with final audio and burn subtitles
            merge_cmd = [
                FFMPEG_EXE, "-y", "-i", temp_vid_no_audio, "-i", target_audio,
                "-vf", f"subtitles={temp_ass}",
                "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", output_vid
            ]
            print(f"Rendering scene {scene_num} with subtitles...")
            res = subprocess.run(merge_cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"FFmpeg Error for scene {scene_num}:\n{res.stderr}")
            
            f.write(f"file '{output_vid}'\n")
            temp_files.extend([temp_fg, temp_vid_no_audio, temp_ass, output_vid])
            
    # Concat segments into final output
    final_output = os.path.join(EXPORT_DIR, "geumdeung_shorts_final.mp4")
    print("Concatenating segments into final video...")
    concat_cmd = [
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path,
        "-c", "copy", final_output
    ]
    res = subprocess.run(concat_cmd, capture_output=True, text=True)
    
    # Cleanup
    for tf in temp_files:
        if os.path.exists(tf):
            os.remove(tf)
    if os.path.exists(concat_list_path):
        os.remove(concat_list_path)
        
    os.chdir(orig_cwd)
    
    if res.returncode == 0:
        print(f"Successfully generated final video: {final_output}")
        return True
    else:
        print(f"Concatenating failed:\n{res.stderr}")
        return False

async def main():
    print("=== STARTING GEUMDEUNGJISA AUTOMATIC BATCH PROCESSING (V3 — RUNWAY INTEGRATED) ===")
    print(f"Runway motion videos directory: {VIDEO_DIR}")
    runway_count = sum(1 for i in range(1, 6) if os.path.exists(os.path.join(VIDEO_DIR, f"scene{i}_motion.mp4")))
    print(f"Runway motion videos available: {runway_count}/5")
    print("")
    scene_words = await generate_tts_from_script()
    success = render_segments(scene_words)
    if success:
        final_path = os.path.join(EXPORT_DIR, "geumdeung_shorts_final.mp4")
        size_mb = os.path.getsize(final_path) / (1024*1024) if os.path.exists(final_path) else 0
        print(f"")
        print(f"=== BATCH PROCESSING COMPLETED SUCCESSFULLY ===")
        print(f"Final video: {final_path}")
        print(f"File size: {size_mb:.1f} MB")
    else:
        print("=== BATCH PROCESSING FAILED ===")

if __name__ == "__main__":
    asyncio.run(main())
