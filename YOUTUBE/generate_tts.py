import asyncio
import edge_tts
import os

# 디렉토리 설정
SHORTS_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\shorts"
LONGFORM_DIR = r"d:\DMDG_UT\YOUTUBE\result\audio\longform"

os.makedirs(SHORTS_DIR, exist_ok=True)
os.makedirs(LONGFORM_DIR, exist_ok=True)

# 1. 쇼츠 대본 설정
shorts_scripts = [
    # KOR (Duffy: InJoon, Voice: SunHi)
    { "file": os.path.join(SHORTS_DIR, "001_shorts_scene1_duffy_KOR.mp3"), "text": "오 마이 갓... 인간들은 왜 이렇게 아름다운 궁궐에서 이런 끔찍하고 소름 돋는 무거운 감정을 느끼는 거죠? 이게 너희가 말하는 '한'인가요?", "voice": "ko-KR-InJoonNeural" },
    { "file": os.path.join(SHORTS_DIR, "002_shorts_scene2_duffy_KOR.mp3"), "text": "진짜 이해할 수 없어... 어? 뭐지?", "voice": "ko-KR-InJoonNeural" },
    { "file": os.path.join(SHORTS_DIR, "003_shorts_scene2_voice_KOR.mp3"), "text": "그 밤, 조선의 국모는 가장 차가운 칼날 앞에 섰지만, 그녀의 마지막 시선은...", "voice": "ko-KR-SunHiNeural" },
    { "file": os.path.join(SHORTS_DIR, "004_shorts_scene3_duffy_KOR.mp3"), "text": "와우. 이 슬픔은... 차원을 넘어선 무언가네요. 대체 이 목소리는 누구죠?", "voice": "ko-KR-InJoonNeural" },
    { "file": os.path.join(SHORTS_DIR, "005_shorts_scene4_narration_KOR.mp3"), "text": "신수 해태마저 울린 이 목소리의 정체와, 숨겨진 조선의 마지막 밤 이야기...", "voice": "ko-KR-SunHiNeural" },
    
    # ENG (Duffy: Brian, Voice: Christopher)
    { "file": os.path.join(SHORTS_DIR, "001_shorts_scene1_duffy_ENG.mp3"), "text": "Oh my god... Why do humans feel such a terrifying and heavy emotion in such a beautiful palace? Is this what you call 'Han'?", "voice": "en-US-BrianNeural" },
    { "file": os.path.join(SHORTS_DIR, "002_shorts_scene2_duffy_ENG.mp3"), "text": "I really can't understand... Huh? What is this?", "voice": "en-US-BrianNeural" },
    { "file": os.path.join(SHORTS_DIR, "003_shorts_scene2_voice_ENG.mp3"), "text": "That night, the mother of Joseon stood before the coldest blade, but her final gaze was...", "voice": "en-US-ChristopherNeural" },
    { "file": os.path.join(SHORTS_DIR, "004_shorts_scene3_duffy_ENG.mp3"), "text": "Wow. This sorrow... it's something beyond dimensions. Whose voice is this?", "voice": "en-US-BrianNeural" },
    { "file": os.path.join(SHORTS_DIR, "005_shorts_scene4_narration_ENG.mp3"), "text": "The true identity of the voice that moved even the divine beast Haetae, and the hidden story of Joseon's final night...", "voice": "en-US-ChristopherNeural" },
    
    # JPN (Duffy: Keita, Voice: Keita)
    { "file": os.path.join(SHORTS_DIR, "001_shorts_scene1_duffy_JPN.mp3"), "text": "オーマイゴッド…人間たちはなぜ、こんなに美しい宮殿でこんなにも恐ろしくて重い感情を抱くの？これが君たちの言う「ハン」なの？", "voice": "ja-JP-KeitaNeural" },
    { "file": os.path.join(SHORTS_DIR, "002_shorts_scene2_duffy_JPN.mp3"), "text": "本当に理解できない…え？何これ？", "voice": "ja-JP-KeitaNeural" },
    { "file": os.path.join(SHORTS_DIR, "003_shorts_scene2_voice_JPN.mp3"), "text": "その夜、朝鮮の国母は最も冷たい刃の前に立ったが、彼女の最後の視線は…", "voice": "ja-JP-KeitaNeural" },
    { "file": os.path.join(SHORTS_DIR, "004_shorts_scene3_duffy_JPN.mp3"), "text": "ワオ。この悲しみは…次元を超えた何かだね。一体この声は誰なの？", "voice": "ja-JP-KeitaNeural" },
    { "file": os.path.join(SHORTS_DIR, "005_shorts_scene4_narration_JPN.mp3"), "text": "神獣ヘテさえも泣かせたこの声の正体と、隠された朝鮮の最後の夜の物語…", "voice": "ja-JP-KeitaNeural" }
]

# 2. 롱폼 대본 설정 (KOR, ENG, JPN)
# KOR: SunHi, ENG: Christopher, JPN: Keita
longform_scripts = [
    # Scene 1
    {
        "file": os.path.join(LONGFORM_DIR, "001_long_scene1_KOR.mp3"),
        "text": "1895년의 가을밤, 건청궁의 공기는 유난히 차가웠습니다. 한 나라의 국모가 머무는 곳이었지만, 그 밤의 정적은 다가올 비극을 예견하듯 무겁게 가라앉아 있었습니다.",
        "voice": "ko-KR-SunHiNeural"
    },
    {
        "file": os.path.join(LONGFORM_DIR, "002_long_scene1_ENG.mp3"),
        "text": "On an autumn night in 1895, the air around Geoncheonggung Palace was unusually cold. Though it was the residence of the nation's mother, the silence of that night hung heavy, as if foreseeing the tragedy to come.",
        "voice": "en-US-ChristopherNeural"
    },
    {
        "file": os.path.join(LONGFORM_DIR, "003_long_scene1_JPN.mp3"),
        "text": "1895年の秋の夜、乾清宮の空気はひときわ冷たく感じられました。一国の国母が留まる場所でありながら、その夜の静寂はやがて訪れる悲劇を予見するかのように重く沈んでいました。",
        "voice": "ja-JP-KeitaNeural"
    },
    # Scene 2
    {
        "file": os.path.join(LONGFORM_DIR, "004_long_scene2_KOR.mp3"),
        "text": "누구도 상상하지 못한 폭력이 가장 깊은 궁궐의 문을 부수고 들어왔습니다. 권력과 야욕이라는 이름 아래, 한 인간의 존엄성은 무참히 짓밟혔습니다. 바닥에 떨어진 옥비녀 위로, 붉은 눈물이 번져갔습니다.",
        "voice": "ko-KR-SunHiNeural"
    },
    {
        "file": os.path.join(LONGFORM_DIR, "005_long_scene2_ENG.mp3"),
        "text": "Unimaginable violence shattered the doors of the deepest palace. Under the guise of power and ambition, a human being's dignity was ruthlessly trampled. Over the jade hairpin fallen on the floor, red tears began to spread.",
        "voice": "en-US-ChristopherNeural"
    },
    {
        "file": os.path.join(LONGFORM_DIR, "006_long_scene2_JPN.mp3"),
        "text": "誰も想像すらできなかった暴力が、最も奥深い宮殿の扉を打ち破って入り込みました。権力と野望という名の下に、一人の人間の尊厳が無惨にも踏みにじられました。床に落ちた玉の簪の上に、赤い涙が滲んでいきました。",
        "voice": "ja-JP-KeitaNeural"
    },
    # Scene 3
    {
        "file": os.path.join(LONGFORM_DIR, "007_long_scene3_KOR.mp3"),
        "text": "그녀가 스러져간 그 자리에, 지금 우리는 서 있습니다. 언어가 다르고 살아온 세상이 달라도, 부당하게 빼앗긴 삶에 대한 슬픔은 국경을 넘어 우리의 마음을 울립니다. 이것이 바로 우리가 나누어야 할 슬픔, '한'입니다.",
        "voice": "ko-KR-SunHiNeural"
    },
    {
        "file": os.path.join(LONGFORM_DIR, "008_long_scene3_ENG.mp3"),
        "text": "In the very place where she fell, we stand today. Though our languages differ and our worlds are worlds apart, the sorrow for a life unjustly taken resonates across borders, touching our hearts. This is the shared sorrow we must embrace, the essence of Han.",
        "voice": "en-US-ChristopherNeural"
    },
    {
        "file": os.path.join(LONGFORM_DIR, "009_long_scene3_JPN.mp3"),
        "text": "彼女が倒れたその場所に、今私たちは立っています。言葉が違い、生きてきた世界が違っても、不当に奪われた命への悲しみは国境を越えて私たちの心を打ちます。これこそが、私たちが分かち合うべき悲しみ、ハンなのです。",
        "voice": "ja-JP-KeitaNeural"
    },
    # Scene 4
    {
        "file": os.path.join(LONGFORM_DIR, "010_long_scene4_KOR.mp3"),
        "text": "아픈 역사를 기억하는 가장 따뜻한 방법은, 서로의 목소리로 그 슬픔을 안아주는 것입니다. 누군가의 상처가 당신의 목소리로 치유될 수 있도록. 지금, 당신의 목소리로 다음 글을 읽어주세요.",
        "voice": "ko-KR-SunHiNeural"
    },
    {
        "file": os.path.join(LONGFORM_DIR, "011_long_scene4_ENG.mp3"),
        "text": "The warmest way to remember a painful history is to embrace that sorrow with each other's voices. So that someone's wound might be healed by your voice. Now, please read the next line with your voice.",
        "voice": "en-US-ChristopherNeural"
    },
    {
        "file": os.path.join(LONGFORM_DIR, "012_long_scene4_JPN.mp3"),
        "text": "痛ましい歴史を記憶する最も温かい方法は、お互いの声でその悲しみを抱きしめることです。誰かの傷が、あなたの声によって癒やされるように。今、あなたの声で次の文章を読んでください。",
        "voice": "ja-JP-KeitaNeural"
    }
]

all_scripts = shorts_scripts + longform_scripts

async def main():
    print(f"Total files to generate: {len(all_scripts)}")
    for item in all_scripts:
        print(f"Generating {os.path.basename(item['file'])} with voice {item['voice']}...")
        communicate = edge_tts.Communicate(item['text'], item['voice'])
        await communicate.save(item['file'])
    print("All TTS generations completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
