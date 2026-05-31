import os
from pydub import AudioSegment

AUDIO_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\longform"
SFX_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\sfx"
BGM_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\bgm"
EXPORT_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\mixed"

if not os.path.exists(EXPORT_DIR): os.makedirs(EXPORT_DIR)

def mix_scene(base_tts_file, bgm_file, sfx_list, output_file):
    print(f"Mixing audio for: {os.path.basename(output_file)}")
    
    # 1. Load base TTS
    if not os.path.exists(base_tts_file):
        print(f"Error: {base_tts_file} not found.")
        return
    base_audio = AudioSegment.from_file(base_tts_file)
    
    # 2. Add BGM (Looping if BGM is shorter than TTS)
    if bgm_file and os.path.exists(bgm_file):
        bgm = AudioSegment.from_file(bgm_file)
        # BGM 볼륨 조절 (TTS가 잘 들리게 낮춤)
        bgm = bgm - 10 
        
        # TTS 길이만큼 BGM 반복
        mixed_audio = base_audio.overlay(bgm, loop=True)
    else:
        mixed_audio = base_audio

    # 3. Add SFX at specific timestamps
    for sfx_path, start_time_ms in sfx_list:
        if os.path.exists(sfx_path):
            sfx = AudioSegment.from_file(sfx_path)
            # SFX를 해당 밀리초(ms) 위치에 덮어씌움
            mixed_audio = mixed_audio.overlay(sfx, position=start_time_ms)
        else:
            print(f"Warning: SFX {sfx_path} not found.")

    # 4. Export
    mixed_audio.export(output_file, format="mp3")
    print(f"Exported: {output_file}")

def main():
    # 예시: KOR 씬 2 (창호지 부서지고 옥비녀 떨어지는 씬) 믹싱
    base_tts = os.path.join(AUDIO_DIR, "004_long_scene2_KOR.mp3")
    bgm = os.path.join(BGM_DIR, "bgm_sad_piano.wav")
    
    # 효과음 타임라인 설정 (효과음 파일 경로, 시작 위치 ms)
    sfx_timeline = [
        (os.path.join(SFX_DIR, "door_crash.wav"), 1000),  # 1초에 문 부서지는 소리
        (os.path.join(SFX_DIR, "sword_draw.wav"), 5000),  # 5초에 칼 뽑는 소리
        (os.path.join(SFX_DIR, "glass_shatter.wav"), 10000) # 10초에 옥비녀 깨지는 소리
    ]
    
    output = os.path.join(EXPORT_DIR, "004_long_scene2_KOR_mixed.mp3")
    mix_scene(base_tts, bgm, sfx_timeline, output)
    
    print("All audio mixing completed.")

if __name__ == "__main__":
    main()
