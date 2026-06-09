import asyncio
import edge_tts
import os

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")

HERMITAGE_AUDIO_DIR = os.path.join(YOUTUBE_DIR, r"Projects\TempleFood\assets_audio")
US_KITCHEN_AUDIO_DIR = os.path.join(YOUTUBE_DIR, r"Projects\TempleFoodUS\assets_audio")

os.makedirs(HERMITAGE_AUDIO_DIR, exist_ok=True)
os.makedirs(US_KITCHEN_AUDIO_DIR, exist_ok=True)

# Hermitage (산속 암자) Script - 5 scenes
hermitage_scripts = [
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene1_KOR.mp3"), "text": "지리산 깊은 암자의 부엌. 자연이 계절에 맞춰 내어준 정직한 재료들이 놓입니다. 나를 낮추고 세상과 연결되는 고요한 시간입니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene1_ENG.mp3"), "text": "A kitchen in a deep mountain hermitage. Honest ingredients, given in accordance with the seasons, are laid out. A quiet time to lower oneself and connect with the world.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene2_KOR.mp3"), "text": "뜨거운 가마솥 안에서 취나물의 쓴맛은 향긋함으로 변하고, 들기름으로 고소함을 더합니다. 세상을 향한 날 선 마음들을 데쳐내어 다스리는 시간입니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene2_ENG.mp3"), "text": "Inside the hot cast-iron pot, the bitterness of Chwinamul turns into fragrance, enriched by savory perilla oil. It is a time to blanch away their sharp edges towards the world.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene3_KOR.mp3"), "text": "두툼한 표고버섯에 달콤한 조청과 간장이 깊이 배어듭니다. 고기 한 점, 마늘 한 톨 없이도, 버섯이 가진 대지의 풍미가 거친 무사의 식탁을 채웁니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene3_ENG.mp3"), "text": "Sweet rice syrup and soy sauce seep deeply into the chewy shiitake mushrooms. Without a single piece of meat or clove of garlic, the earthy flavor of the mushrooms fills the weary hunter's table.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene4_KOR.mp3"), "text": "달큰한 단호박과 옹심이가 들깨의 품에서 걸쭉하게 끓어오릅니다. 비우고 채워내는 산사의 따뜻한 온기가 서씨의 깊은 상처를 어루만집니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene4_ENG.mp3"), "text": "Sweet pumpkin and dough balls boil in the savory embrace of perilla seeds. The warm comfort of the temple, of emptying and filling, gently caresses Seo-ssi's deep scars.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene5_KOR.mp3"), "text": "오늘 하루, 복잡한 세상의 짐을 내려놓고 마음을 비워내는 사찰 요리 어떠신가요? 평온한 산사로 당신을 초대합니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(HERMITAGE_AUDIO_DIR, "scene5_ENG.mp3"), "text": "How about a temple dish to lightly empty your mind today? We invite you to this peaceful mountain temple.", "voice": "en-US-BrianNeural"}
]

# US Kitchen (미국 주방) Script - 8 scenes
us_kitchen_scripts = [
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene1_KOR.mp3"), "text": "지친 일상을 정화하는 더피의 소소 밥상. 오늘은 미국의 마트에서 맑은 공양을 위한 장보기가 시작됩니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene1_ENG.mp3"), "text": "Duffy's Soso Table to purify your weary days. Today, a grocery shopping journey for a pure temple meal begins in an American store.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene2_KOR.mp3"), "text": "한국의 전통 산나물 대신, 미국 마트의 싱싱한 케일과 버터넛 스쿼시가 서씨와 더피의 솜씨로 맑은 사찰음식이 됩니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene2_ENG.mp3"), "text": "Instead of traditional wild herbs, fresh kale and butternut squash from a US store will become pure temple food in the hands of Seo-ssi and Duffy.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene3_KOR.mp3"), "text": "케일은 흐르는 물에 씻어 억센 줄기를 도려내고 부드러운 잎사귀만 남깁니다. 손길 끝에 정성을 다하는 시간입니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene3_ENG.mp3"), "text": "Clean the kale under running water, trim away the tough stems, and keep only the tender leaves. A time of dedication at their fingertips.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene4_KOR.mp3"), "text": "마늘과 파를 완전히 빼낸 빈자리에 생강과 들기름의 깊은 맛이 스며들도록, 작은 채소들을 정성껏 다듬어 나갑니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene4_ENG.mp3"), "text": "Leaving out all garlic and onions, they carefully prep the small vegetables to absorb the deep aromas of ginger and perilla oil.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene5_KOR.mp3"), "text": "두꺼운 껍질 속 드러난 단호박의 노란 속살을 먹기 좋은 크기로 썰어냅니다. 버려지는 것 없이 재료의 본질을 살립니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene5_ENG.mp3"), "text": "Peeling away the tough skin to reveal the golden flesh, slicing it into bite-sized pieces. Preserving the essence without wasting a thing.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene6_KOR.mp3"), "text": "뜨거운 김 속에서 끓어오르는 맑은 온기. 고기 한 점 없이도 스쿼시의 단맛과 들깨의 걸쭉함이 주방을 가득 채웁니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene6_ENG.mp3"), "text": "A pure warmth boiling inside the gentle steam. Even without a single piece of meat, the sweetness of squash and richness of perilla seed fills the kitchen.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene7_KOR.mp3"), "text": "이방인 친구 바비와 한의사 허용준 원장이 함께 마주 앉은 식탁. 낯선 이국 땅에서 소박한 자연의 밥상이 그들을 위로합니다.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene7_ENG.mp3"), "text": "A table shared with their foreign friend Bobby and Korean doctor Heo Yong-joon. In this unfamiliar land, a simple table of nature comforts them.", "voice": "en-US-BrianNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene8_KOR.mp3"), "text": "오늘 저녁은 당신의 주방에 오신채 없는 평온한 밥상을 올려보는 건 어떨까요? 더피의 소소 밥상 완성.", "voice": "ko-KR-InJoonNeural"},
    {"file": os.path.join(US_KITCHEN_AUDIO_DIR, "scene8_ENG.mp3"), "text": "Tonight, why not set a peaceful, allium-free table in your kitchen? Duffy's Soso Table is served.", "voice": "en-US-BrianNeural"}
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
