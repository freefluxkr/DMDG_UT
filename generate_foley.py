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

# 1. Cute Boing (뿅!) - High freq sweeping up
def generate_cute_boing():
    duration = 0.3
    samples = []
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 400 + (t * 2000)  # Sweep up
        env = math.exp(-10 * t)         
        val = math.sin(2 * math.pi * freq * t) * env * 25000
        samples.append(val)
    save_wav('C:\\Users\\tuesv\\Documents\\DMDG_UT\\cute_boing.wav', samples)

# 2. Cute Poing (띠용~) - Sine wave with pitch modulation
def generate_cute_poing():
    duration = 0.4
    samples = []
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 300 + math.sin(t * 30) * 100
        env = math.exp(-8 * t)
        val = math.sin(2 * math.pi * freq * t) * env * 25000
        samples.append(val)
    save_wav('C:\\Users\\tuesv\\Documents\\DMDG_UT\\cute_poing.wav', samples)

# 3. Magic Sparkle (샤라랑~) - High freq noise with sine bursts
def generate_magic_sparkle():
    duration = 0.5
    samples = []
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 4000 + random.uniform(-500, 500)
        env = math.exp(-5 * t) * (0.5 + 0.5 * math.sin(t * 50))
        val = math.sin(2 * math.pi * freq * t) * env * 15000
        samples.append(val)
    save_wav('C:\\Users\\tuesv\\Documents\\DMDG_UT\\magic_sparkle.wav', samples)

if __name__ == "__main__":
    generate_cute_boing()
    generate_cute_poing()
    generate_magic_sparkle()
    print("Generated 3 cute cartoon Foley ASMR sound files! (boing, poing, sparkle)")
