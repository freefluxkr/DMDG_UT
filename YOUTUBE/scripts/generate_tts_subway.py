import asyncio
import edge_tts
import os

# 디렉토리 설정 (새로운 프로젝트 구조)
BASE_DIR = r"C:\Users\user\Documents\DMDG_UT"
AUDIO_DIR = os.path.join(BASE_DIR, r"YOUTUBE\Projects\Subway_Shorts\assets_audio")

os.makedirs(AUDIO_DIR, exist_ok=True)

# 강하루 나레이션 대본 (KOR, ENG, JPN)
# 강하루 목소리 설정: 약간 시니컬하고 차분한 톤
scripts = [
    # KOR (Voice: InJoon)
    { 
        "file": os.path.join(AUDIO_DIR, "001_subway_scene1_KOR.mp3"), 
        "text": "서울의 지하로 내려가는 건, 거대한 콘크리트 위장에 삼켜지는 것과 비슷하다. 그곳에는 특유의 메마른 규칙이 존재한다.", 
        "voice": "ko-KR-InJoonNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "002_subway_scene2_KOR.mp3"), 
        "text": "사람들은 마찰력을 상실한 당구공처럼 서로의 어깨를 퍽, 퍽 부딪치며 튕겨져 나간다. 일본 도쿄를 공포로 몰아넣은 '부츠카리 오토코'의 그림자가, 이곳에서도 어김없이 배회하고 있다. 사과 같은 건 없다. 미안하다는 말은 사치품이니까.", 
        "voice": "ko-KR-InJoonNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "003_subway_scene3_KOR.mp3"), 
        "text": "환승 계단 앞에서는 기묘한 집단 최면이 일어난다. 한 명이 틈새를 파고들면, 뒤따르던 이들이 물을 만난 연어 떼처럼 합류해 거대한 새치기의 강물을 만든다. 줄을 서는 자만 어리석은 섬으로 남겨지는 기이한 풍경.", 
        "voice": "ko-KR-InJoonNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "004_subway_scene4_KOR.mp3"), 
        "text": "가장 깊고 빠른 지하철. 그곳의 경로석은 노이즈 캔슬링 이어폰을 낀 젊은 귀족들의 차지다. 눈을 감고 귀를 막으면, 타인의 무게감은 이 세계에서 완벽하게 증발해 버린다.", 
        "voice": "ko-KR-InJoonNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "005_subway_outro_KOR.mp3"), 
        "text": "초속 100km로 달리는 도시. 우리는 너무 빨리 가려다, 무언가 중요한 것을 승강장에 떨어뜨리고 온 것은 아닐까? 당신의 출근길은, 안녕하십니까.", 
        "voice": "ko-KR-InJoonNeural" 
    },
    
    # ENG (Voice: Brian)
    { 
        "file": os.path.join(AUDIO_DIR, "001_subway_scene1_ENG.mp3"), 
        "text": "Descending into Seoul's underground is like being swallowed by a giant concrete stomach. A peculiar, dry set of rules exists there.", 
        "voice": "en-US-BrianNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "002_subway_scene2_ENG.mp3"), 
        "text": "People bounce off each other like frictionless billiard balls, slamming shoulders. The shadow of Tokyo's 'Butsukari Otoko' roams freely here too. There are no apologies. Saying 'sorry' is a luxury.", 
        "voice": "en-US-BrianNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "003_subway_scene3_ENG.mp3"), 
        "text": "A bizarre mass hypnosis occurs at the transfer stairs. When one person cuts in, others follow like a school of salmon, creating a massive river of line-cutters. A strange scene where only those who wait in line are left as fools.", 
        "voice": "en-US-BrianNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "004_subway_scene4_ENG.mp3"), 
        "text": "The deepest and fastest subway. Its priority seating belongs to young nobles wearing noise-canceling earphones. Close your eyes and block your ears, and the weight of others perfectly evaporates from this world.", 
        "voice": "en-US-BrianNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "005_subway_outro_ENG.mp3"), 
        "text": "A city running at 100km/h. In our rush, have we dropped something crucial on the platform? How is your morning commute?", 
        "voice": "en-US-BrianNeural" 
    },
    
    # JPN (Voice: Keita)
    { 
        "file": os.path.join(AUDIO_DIR, "001_subway_scene1_JPN.mp3"), 
        "text": "ソウルの地下へ降りていくのは、巨大なコンクリートの胃袋に飲み込まれるようなものだ。そこには特有の乾いたルールが存在する。", 
        "voice": "ja-JP-KeitaNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "002_subway_scene2_JPN.mp3"), 
        "text": "人々は摩擦を失ったビリヤードの球のように、肩を激しくぶつけ合いながら弾き飛ばされる。東京を恐怖に陥れた『ぶつかり男』の影が、ここでも間違いなく徘徊している。謝罪などない。ごめんなさいという言葉は贅沢品だからだ。", 
        "voice": "ja-JP-KeitaNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "003_subway_scene3_JPN.mp3"), 
        "text": "乗り換え階段の前では、奇妙な集団催眠が起こる。一人が隙間に入り込むと、後ろの者たちが水を得た鮭の群れのように合流し、巨大な割り込みの川を作る。列に並ぶ者だけが愚かな島として取り残される奇怪な風景。", 
        "voice": "ja-JP-KeitaNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "004_subway_scene4_JPN.mp3"), 
        "text": "最も深くて速い地下鉄。そこの優先席はノイズキャンセリングイヤホンをつけた若い貴族たちのものだ。目を閉じ、耳を塞げば、他人の重みはこの世界から完全に蒸発してしまう。", 
        "voice": "ja-JP-KeitaNeural" 
    },
    { 
        "file": os.path.join(AUDIO_DIR, "005_subway_outro_JPN.mp3"), 
        "text": "秒速100kmで走る都市。私たちは急ぐあまり、何か重要なものをホームに落としてきたのではないだろうか？ あなたの通勤路は、ご無事ですか。", 
        "voice": "ja-JP-KeitaNeural" 
    }
]

async def main():
    print(f"Total files to generate for Subway Shorts: {len(scripts)}")
    for item in scripts:
        print(f"Generating {os.path.basename(item['file'])} with voice {item['voice']}...")
        
        # 강하루 캐릭터에 맞게 약간 무미건조하고 차분한 톤으로 세팅
        rate = "-0%"   
        pitch = "-5Hz" 
            
        communicate = edge_tts.Communicate(item['text'], item['voice'], rate=rate, pitch=pitch)
        await communicate.save(item['file'])
    print("All Subway TTS generations completed successfully in Projects/Subway_Shorts/assets_audio.")

if __name__ == "__main__":
    asyncio.run(main())
