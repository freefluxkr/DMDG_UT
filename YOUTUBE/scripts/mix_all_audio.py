import os
import subprocess

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE"
AUDIO_DIR = os.path.join(BASE_DIR, r"Projects\Empress_Longform\assets_audio")
SFX_DIR = os.path.join(BASE_DIR, r"result\audio\sfx")
BGM_DIR = os.path.join(BASE_DIR, r"result\audio\bgm")
FFMPEG_EXE = os.path.join(BASE_DIR, "ffmpeg.exe")

def mix_scene_ffmpeg(base_tts_file, bgm_file, sfx_list, output_file):
    print(f"Mixing audio for: {os.path.basename(output_file)}")
    
    if not os.path.exists(base_tts_file):
        print(f"Error: {base_tts_file} not found.")
        return

    inputs = ["-y", "-i", base_tts_file]
    filter_complex = ""
    amix_inputs = "[0:a]"
    input_idx = 1
    
    # Add BGM
    if bgm_file and os.path.exists(bgm_file):
        inputs.extend(["-stream_loop", "-1", "-i", bgm_file])
        # volume 0.15 is roughly -15dB, lower BGM volume
        filter_complex += f"[{input_idx}:a]volume=0.15[bgm];"
        amix_inputs += "[bgm]"
        input_idx += 1

    # Add SFX
    sfx_labels = []
    for sfx_path, start_time_ms in sfx_list:
        if os.path.exists(sfx_path):
            inputs.extend(["-i", sfx_path])
            label = f"sfx{input_idx}"
            # delay requires milliseconds, volume controls SFX loudness (increased from 0.8 to 2.5)
            filter_complex += f"[{input_idx}:a]adelay={start_time_ms}|{start_time_ms},volume=2.5[{label}];"
            amix_inputs += f"[{label}]"
            input_idx += 1
        else:
            print(f"Warning: SFX {sfx_path} not found.")

    if input_idx > 1:
        # Mix all inputs
        filter_complex += f"{amix_inputs}amix=inputs={input_idx}:duration=first:dropout_transition=2[outa]"
        
        cmd = [FFMPEG_EXE] + inputs + [
            "-filter_complex", filter_complex,
            "-map", "[outa]",
            "-c:a", "libmp3lame", "-q:a", "2",
            output_file
        ]
    else:
        # Just copy if no bgm or sfx
        cmd = [FFMPEG_EXE] + inputs + ["-c:a", "copy", output_file]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Exported: {output_file}")
    else:
        print(f"Error mixing {output_file}:\n{result.stderr}")

def main():
    languages = ["KOR", "ENG", "JPN"]
    bgm = os.path.join(BGM_DIR, "bgm_sad_piano.wav")
    
    # Scene 2 SFX timeline
    sfx_scene2 = [
        (os.path.join(SFX_DIR, "door_crash.wav"), 1000),
        (os.path.join(SFX_DIR, "footstep.wav"), 3000),
        (os.path.join(SFX_DIR, "sword_draw.wav"), 5000),
        (os.path.join(SFX_DIR, "glass_shatter.wav"), 7000)
    ]
    
    for lang in languages:
        for scene_num in range(1, 5):
            audio_idx = (scene_num - 1) * 3 + 1
            if lang == "ENG": audio_idx += 1
            if lang == "JPN": audio_idx += 2
            
            base_tts = os.path.join(AUDIO_DIR, f"{audio_idx:03d}_long_scene{scene_num}_{lang}.mp3")
            output = os.path.join(AUDIO_DIR, f"{audio_idx:03d}_long_scene{scene_num}_{lang}_mixed.mp3")
            
            if scene_num == 2:
                mix_scene_ffmpeg(base_tts, bgm, sfx_scene2, output)
            else:
                mix_scene_ffmpeg(base_tts, bgm, [], output)
                
    print("All audio mixing completed with FFmpeg.")

if __name__ == "__main__":
    main()
