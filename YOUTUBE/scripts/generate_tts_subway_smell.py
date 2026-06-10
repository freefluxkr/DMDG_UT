import asyncio
import edge_tts
import os

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
AUDIO_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Subway_Smell\assets_audio")

os.makedirs(AUDIO_DIR, exist_ok=True)

scripts = [
    {
        "file": os.path.join(AUDIO_DIR, "001_subway_scene1_KOR.mp3"),
        "text": "지하철 문이 열리는 순간 시작되는 소리 없는 전쟁. 바로 옆 사람의 냄새입니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(AUDIO_DIR, "002_subway_scene2_KOR.mp3"),
        "text": "레딧과 SNS를 뜨겁게 달군 3대 냄새 빌런! 한여름 땀 찌든 내, 덜 마른 옷의 퀴퀴한 쉰내, 그리고 좁은 밀폐 공간을 마비시키는 독한 향수 폭탄까지.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(AUDIO_DIR, "003_subway_scene3_KOR.mp3"),
        "text": "예방법은 간단합니다. 쉰내 나는 옷은 섬유유연제로 덮지 말고, 베이킹소다나 온수 세탁으로 균을 확실히 잡으세요. 향수는 탑승 30분 전에 가볍게만 뿌리는 배려가 필요합니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(AUDIO_DIR, "004_subway_scene4_KOR.mp3"),
        "text": "피할 수 없다면 방어하세요! 코밑에 민트나 레몬 향 멀티밤을 살짝 바르거나, 휴대용 마스크를 착용하는 것만으로도 나만의 쾌적한 방어막을 구축할 수 있습니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(AUDIO_DIR, "005_subway_outro_KOR.mp3"),
        "text": "나를 향한 관리와 타인을 향한 배려로 더욱 향기로운 하루를 만들어보세요. 구독하고 더 많은 일상 매너 팁을 만나보세요!",
        "voice": "ko-KR-InJoonNeural"
    }
]

async def main():
    print(f"Starting Subway Smell TTS Generation. Total tasks: {len(scripts)}")
    for item in scripts:
        print(f"Generating: {os.path.basename(item['file'])} ...")
        
        # Pacing settings
        rate = "-5%"
        pitch = "-5Hz"
        
        try:
            communicate = edge_tts.Communicate(item['text'], item['voice'], rate=rate, pitch=pitch)
            await communicate.save(item['file'])
            print(f"Saved: {item['file']}")
        except Exception as e:
            print(f"Error generating TTS for {item['file']}: {e}")
            
    print("All Subway Smell TTS audio files generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
