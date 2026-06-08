import asyncio
import edge_tts
import os

# Directories for audio assets
BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")

HERMITAGE_AUDIO_DIR = os.path.join(YOUTUBE_DIR, r"Projects\TempleFood\assets_audio")
US_KITCHEN_AUDIO_DIR = os.path.join(YOUTUBE_DIR, r"Projects\TempleFoodUS\assets_audio")

os.makedirs(HERMITAGE_AUDIO_DIR, exist_ok=True)
os.makedirs(US_KITCHEN_AUDIO_DIR, exist_ok=True)

# 1. Hermitage (산속 암자) Script
hermitage_scripts = [
    # Scene 1
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene1_KOR.mp3"),
        "text": "지리산 깊은 암자의 부엌. 자연이 계절에 맞춰 내어준 정직한 재료들이 놓입니다. 나를 낮추고 세상과 연결되는 고요한 시간입니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene1_ENG.mp3"),
        "text": "A kitchen in a deep mountain hermitage. Honest ingredients, given in accordance with the seasons, are laid out. A quiet time to lower oneself and connect with the world.",
        "voice": "en-US-BrianNeural"
    },
    # Scene 2
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene2_KOR.mp3"),
        "text": "뜨거운 가마솥 안에서 취나물의 쓴맛은 향긋함으로 변하고, 들기름으로 고소함을 더합니다. 세상을 향한 날 선 마음들을 데쳐내어 다스리는 시간입니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene2_ENG.mp3"),
        "text": "Inside the hot cast-iron pot, the bitterness of Chwinamul turns into fragrance, enriched by savory perilla oil. It is a time to blanch away their sharp edges towards the world.",
        "voice": "en-US-BrianNeural"
    },
    # Scene 3
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene3_KOR.mp3"),
        "text": "두툼한 표고버섯에 달콤한 조청과 간장이 깊이 배어듭니다. 고기 한 점, 마늘 한 톨 없이도, 버섯이 가진 대지의 풍미가 거친 무사의 식탁을 채웁니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene3_ENG.mp3"),
        "text": "Sweet rice syrup and soy sauce seep deeply into the chewy shiitake mushrooms. Without a single piece of meat or clove of garlic, the earthy flavor of the mushrooms fills the weary hunter's table.",
        "voice": "en-US-BrianNeural"
    },
    # Scene 4
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene4_KOR.mp3"),
        "text": "달큰한 단호박과 옹심이가 들깨의 품에서 걸쭉하게 끓어오릅니다. 비우고 채워내는 산사의 따뜻한 온기가 서씨의 깊은 상처를 어루만집니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene4_ENG.mp3"),
        "text": "Sweet pumpkin and dough balls boil in the savory embrace of perilla seeds. The warm comfort of the temple, of emptying and filling, gently caresses Seo-ssi's deep scars.",
        "voice": "en-US-BrianNeural"
    },
    # Scene 5 (Outro)
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene5_KOR.mp3"),
        "text": "오늘 하루, 복잡한 세상의 짐을 내려놓고 마음을 비워내는 사찰 요리 어떠신가요? 평온한 산사로 당신을 초대합니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(HERMITAGE_AUDIO_DIR, "scene5_ENG.mp3"),
        "text": "How about a temple dish to lightly empty your mind today? We invite you to this peaceful mountain temple.",
        "voice": "en-US-BrianNeural"
    }
]

# 2. US Kitchen (미국 주방) Script - Duffy's Soso Table
us_kitchen_scripts = [
    # Scene 1 (Hook/Intro)
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene1_KOR.mp3"),
        "text": "지친 일상을 정화하는 더피의 소소 밥상. 미국 마트의 애호박, 버섯, 당근이 서씨와 더피의 솜씨로 맑은 사찰음식이 됩니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene1_ENG.mp3"),
        "text": "Duffy's Soso Table to purify your weary days. Zucchini, mushrooms, and carrots from a US store become pure temple food in the hands of Seo-ssi and Duffy.",
        "voice": "en-US-BrianNeural"
    },
    # Scene 2 (Zucchini & Mushrooms)
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene2_KOR.mp3"),
        "text": "마늘, 파, 양파 같은 오신채는 절대 넣지 않습니다. 들기름과 고추로만 버무려 낸 구운 애호박 버섯 무침. 비워낼수록 깊어지는 맛입니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene2_ENG.mp3"),
        "text": "No garlic, no onions—the five pungent spices are completely excluded. Mixed only with perilla oil and chili, this grilled zucchini and mushroom dish tastes deeper as it empties.",
        "voice": "en-US-BrianNeural"
    },
    # Scene 3 (Carrot Pancake)
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene3_KOR.mp3"),
        "text": "당근 본연의 달큰한 맛을 온전히 살린 선재스님의 당근전. 화려함 대신 소박함을 담아 바삭하게 구워냅니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene3_ENG.mp3"),
        "text": "Ven. Sunjae's carrot pancake, fully preserving the natural sweetness of carrots. Baked to crispy perfection, embracing simplicity instead of extravagance.",
        "voice": "en-US-BrianNeural"
    },
    # Scene 4 (Potato & Lotus Root)
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene4_KOR.mp3"),
        "text": "해외를 울린 정관스님의 레시피. 감자를 갈아 부친 쫄깃한 감자전과 고소한 연근 호두 조림이 낯선 이국 땅에 따스한 온기를 채웁니다.",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene4_ENG.mp3"),
        "text": "Ven. Jeong Kwan's recipe that moved the world. Chewy potato pancake and savory braised lotus root with walnuts fill this unfamiliar land with warm comfort.",
        "voice": "en-US-BrianNeural"
    },
    # Scene 5 (Outro)
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene5_KOR.mp3"),
        "text": "오늘 저녁은 당신의 주방에 오신채 없는 평온한 밥상을 올려보는 건 어떨까요?",
        "voice": "ko-KR-InJoonNeural"
    },
    {
        "file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene5_ENG.mp3"),
        "text": "Tonight, why not set a peaceful, allium-free table in your kitchen?",
        "voice": "en-US-BrianNeural"
    }
]

all_scripts = hermitage_scripts + us_kitchen_scripts

async def main():
    print(f"Starting Temple Food TTS Generation. Total tasks: {len(all_scripts)}")
    for item in all_scripts:
        print(f"Generating: {os.path.basename(item['file'])} ...")
        
        # Meditative and calm pacing (-10% rate, -10Hz pitch for solemnity)
        rate = "-10%"
        pitch = "-10Hz"
        
        try:
            communicate = edge_tts.Communicate(item['text'], item['voice'], rate=rate, pitch=pitch)
            await communicate.save(item['file'])
            print(f"Saved: {item['file']}")
        except Exception as e:
            print(f"Error generating TTS for {item['file']}: {e}")
            
    print("All Temple Food TTS audio files generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
