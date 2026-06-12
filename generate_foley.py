import wave
import math
import random
import struct

SAMPLE_RATE = 44100

def save_wav(filename, samples):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        for s in samples:
            f.writeframesraw(struct.pack('<h', int(max(-32767, min(32767, s)))))

# 1. Wood Tock (나무 블록 소리) - Low freq sine with fast exponential decay
def generate_wood_tock():
    duration = 0.15
    samples = []
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 400 * math.exp(-20 * t)  # Pitch drop
        env = math.exp(-30 * t)         # Fast decay
        val = math.sin(2 * math.pi * freq * t) * env * 25000
        samples.append(val)
    save_wav('C:\\Users\\tuesv\\Documents\\DMDG_UT\\wood_tock.wav', samples)

# 2. Clay Slap (찰흙 부딪히는 소리) - Noise with lowpass filter and envelope
def generate_clay_slap():
    duration = 0.2
    samples = []
    last_val = 0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        env = math.exp(-25 * t)
        # generate noise
        noise = random.uniform(-1, 1)
        # simple lowpass
        val = (noise * 0.2 + last_val * 0.8)
        last_val = val
        samples.append(val * env * 30000)
    save_wav('C:\\Users\\tuesv\\Documents\\DMDG_UT\\clay_slap.wav', samples)

# 3. Magnetic Click (자석 찰칵 소리) - High freq short burst
def generate_magnetic_click():
    duration = 0.05
    samples = []
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 3000
        env = math.exp(-100 * t)
        val = math.sin(2 * math.pi * freq * t) * env * 20000
        samples.append(val)
    save_wav('C:\\Users\\tuesv\\Documents\\DMDG_UT\\magnetic_click.wav', samples)

generate_wood_tock()
generate_clay_slap()
generate_magnetic_click()

print("Generated 3 distinct Foley ASMR sound files!")
