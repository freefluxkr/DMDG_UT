import wave
import math
import struct
import os

def create_beep(filename, freq=440, duration=1.0, volume=0.5):
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1) # mono
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Generate sine wave
            value = int(volume * 32767.0 * math.sin(2.0 * math.pi * freq * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

SFX_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\sfx"
BGM_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\bgm"

if not os.path.exists(SFX_DIR): os.makedirs(SFX_DIR)
if not os.path.exists(BGM_DIR): os.makedirs(BGM_DIR)

print("Generating dummy SFX and BGM files...")
create_beep(os.path.join(BGM_DIR, "bgm_sad_piano.wav"), freq=220, duration=10.0, volume=0.1) # 10s low beep
create_beep(os.path.join(BGM_DIR, "bgm_wind.wav"), freq=110, duration=10.0, volume=0.1)

create_beep(os.path.join(SFX_DIR, "footstep.wav"), freq=150, duration=0.5, volume=0.3)
create_beep(os.path.join(SFX_DIR, "door_crash.wav"), freq=300, duration=0.8, volume=0.5)
create_beep(os.path.join(SFX_DIR, "sword_draw.wav"), freq=880, duration=1.0, volume=0.4)
create_beep(os.path.join(SFX_DIR, "glass_shatter.wav"), freq=1200, duration=0.6, volume=0.4)

print("Dummy audio files created successfully!")
