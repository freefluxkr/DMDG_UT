import asyncio
import edge_tts
import os

AUDIO_DIR = r"c:\Users\user\Documents\DMDG_UT\YOUTUBE\Projects\Empress_Longform\assets_audio"

scripts = [
    # KOR
    {
        "file": os.path.join(AUDIO_DIR, "007_long_scene3_KOR.mp3"),
        "text": "그녀가 스러져간 그 자리에, 지금 우리는 서 있습니다. 수많은 계절이 바뀌고 백 년의 세월이 흘렀지만, 그날 밤 흩날리던 슬픔의 조각들은 여전히 이 궁궐 어귀에 남아 있습니다. 언어가 다르고 살아온 세상이 달라도, 부당하게 빼앗긴 삶에 대한 아픔은 국경을 넘어 우리의 마음을 울립니다. 이 깊은 먹먹함, 이토록 찬란하고도 서글픈 공감대... 이것이 바로 우리가 함께 나누고 위로해야 할 조선의 슬픔, '한'입니다.",
        "voice": "ko-KR-SunHiNeural"
    },
    {
        "file": os.path.join(AUDIO_DIR, "010_long_scene4_KOR.mp3"),
        "text": "아픈 역사를 기억하는 가장 따뜻한 방법은 무엇일까요? 그것은 바로 서로의 목소리로, 과거의 멍든 슬픔을 조용히 안아주는 것입니다. 누군가의 깊은 상처가, 오늘을 살아가는 당신의 따뜻한 목소리로 치유될 수 있도록. 이제는 당신이 이 이야기의 화자가 되어주실 차례입니다. 지금 화면을 두 번 터치하여 당신의 목소리로 다음 글을 읽어주세요.",
        "voice": "ko-KR-SunHiNeural"
    },
    # ENG
    {
        "file": os.path.join(AUDIO_DIR, "008_long_scene3_ENG.mp3"),
        "text": "In the very place where she fell, we stand today. Countless seasons have passed and a century has flowed by, yet the fragments of sorrow scattered that night still linger at the edge of this palace. Though our languages differ and our worlds are worlds apart, the pain of a life unjustly taken resonates across borders, touching our hearts. This deep profoundness, this brilliantly sorrowful empathy... This is the shared sorrow of Joseon we must comfort together, the essence of 'Han'.",
        "voice": "en-US-ChristopherNeural"
    },
    {
        "file": os.path.join(AUDIO_DIR, "011_long_scene4_ENG.mp3"),
        "text": "What is the warmest way to remember a painful history? It is to embrace the bruised sorrow of the past quietly with each other's voices. So that someone's deep wound might be healed by your warm voice living today. Now, it is your turn to become the narrator of this story. Please double tap the screen right now and read the next line with your voice.",
        "voice": "en-US-ChristopherNeural"
    },
    # JPN
    {
        "file": os.path.join(AUDIO_DIR, "009_long_scene3_JPN.mp3"),
        "text": "彼女が倒れたその場所に、今私たちは立っています。数え切れないほどの季節が巡り、百年の歳月が流れましたが、あの夜に散った悲しみのかけらは、未だにこの宮殿の片隅に残っています。言葉が違い、生きてきた世界が違っても、不当に奪われた命への痛みは国境を越えて私たちの心を打ちます。この深い胸の詰まり、これほどまでに美しくも切ない共感… これこそが、私たちが共に分かち合い慰め合うべき朝鮮の悲しみ、「恨（ハン）」なのです。",
        "voice": "ja-JP-KeitaNeural"
    },
    {
        "file": os.path.join(AUDIO_DIR, "012_long_scene4_JPN.mp3"),
        "text": "痛ましい歴史を記憶する最も温かい方法は何でしょうか？ それは、お互いの声で、過去の傷ついた悲しみを静かに抱きしめることです。誰かの深い傷が、今日を生きるあなたの温かい声によって癒やされるように。今度は、あなたがこの物語の語り手になる番です。今すぐ画面を2回タッチして、あなたの声で次の文章を読んでください。",
        "voice": "ja-JP-KeitaNeural"
    }
]

async def main():
    print("Regenerating scene 3 & 4 with expanded script and faster pacing...")
    for item in scripts:
        print(f"Generating {os.path.basename(item['file'])}...")
        # Reduce the massive slow down from -15% to -5% so it's not overly boring
        communicate = edge_tts.Communicate(item['text'], item['voice'], rate="-5%", pitch="-10Hz")
        await communicate.save(item['file'])
    print("TTS completed!")

if __name__ == "__main__":
    asyncio.run(main())
