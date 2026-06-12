import random

words_data = [
    ('ㄱ', 'ㅏ', '가', 'Go / Leave', '힘차게 떠나보자!'),
    ('ㄴ', 'ㅏ', '나', 'Me / I', '세상의 중심은 바로 나!'),
    ('ㄷ', 'ㅏ', '다', 'All / Everything', '우리 모두 다 함께!'),
    ('ㄹ', 'ㅏ', '라', 'La (Music note)', '신나게 노래해, 라라라~'),
    ('ㅁ', 'ㅏ', '마', 'Do not (Stop)', '안 돼! 하지 마!'),
    ('ㅂ', 'ㅏ', '바', 'Bar / Look', '저기 좀 봐바!'),
    ('ㅅ', 'ㅏ', '사', 'Buy / Four', '만나서 반가워, 사랑해!'),
    ('ㅇ', 'ㅏ', '아', 'Ah! (Exclamation)', '아! 그렇구나!'),
    ('ㅈ', 'ㅏ', '자', 'Sleep / Ruler', '쿨쿨 잘 자요~'),
    ('ㅊ', 'ㅏ', '차', 'Car / Tea', '따뜻한 차 한잔 어때?'),
    ('ㅋ', 'ㅏ', '카', 'Car (Loanword)', '부릉부릉, 신나는 드라이브!'),
    ('ㅌ', 'ㅏ', '타', 'Ride', '우리 같이 타볼까?'),
    ('ㅍ', 'ㅏ', '파', 'Green Onion', '푸릇푸릇한 파!'),
    ('ㅎ', 'ㅏ', '하', 'Ha (Laugh)', '한바탕 맑게 웃어보자!'),
    ('ㄱ', 'ㅗ', '고', 'High / Go', '높이높이, 고고!'),
    ('ㄴ', 'ㅗ', '노', 'No / Oar', '노노! 그건 아니야!'),
    ('ㄷ', 'ㅗ', '도', 'Island / Way', '여기도, 저기도!'),
    ('ㄹ', 'ㅗ', '로', 'Path / Road', '새로운 길로 떠나요!'),
    ('ㅁ', 'ㅗ', '모', 'Mother / Hair', '모두 모여라!'),
    ('ㅂ', 'ㅗ', '보', 'See / Look', '내 맘을 보여줄게!'),
    ('ㅅ', 'ㅗ', '소', 'Cow', '음메~ 듬직한 소!'),
    ('ㅇ', 'ㅗ', '오', 'Five / Oh!', '오! 놀라워라!'),
    ('ㅈ', 'ㅗ', '조', 'Bird / Trillion', '짹짹, 귀여운 새!'),
    ('ㅊ', 'ㅗ', '초', 'Candle / Seconds', '반짝반짝 빛나는 초!'),
    ('ㅋ', 'ㅗ', '코', 'Nose', '냄새를 맡아봐, 코!'),
    ('ㅌ', 'ㅗ', '토', 'Earth / Soil', '토낏토낏 뛰어보자!'),
    ('ㅍ', 'ㅗ', '포', 'Cannon / Grape', '포도처럼 달콤해!'),
    ('ㅎ', 'ㅗ', '호', 'Lake / Tiger', '호호 불어 먹어요!'),
    ('ㄱ', 'ㅣ', '기', 'Energy / Flag', '기운 내, 파이팅!'),
    ('ㄴ', 'ㅣ', '니', 'You (informal)', '니가 참 좋아!'),
    ('ㄷ', 'ㅣ', '디', 'D (Letter)', '디자인이 예뻐요!'),
    ('ㄹ', 'ㅣ', '리', 'Village (Unit)', '우리 마을로 오세요!'),
    ('ㅁ', 'ㅣ', '미', 'Beauty', '아름다운 미소!'),
    ('ㅂ', 'ㅣ', '비', 'Rain', '촉촉하게 비 내리는 마을'),
    ('ㅅ', 'ㅣ', '시', 'Time / Poem', '시간이 참 빨라요!'),
    ('ㅇ', 'ㅣ', '이', 'Two / Teeth', '이런, 깜짝야!'),
    ('ㅈ', 'ㅣ', '지', 'Earth / Wisdom', '지금 바로 시작해!'),
    ('ㅊ', 'ㅣ', '치', 'Value / Heal', '치즈~ 웃어보세요!'),
    ('ㅋ', 'ㅣ', '키', 'Key / Height', '키가 쑥쑥 자라요!'),
    ('ㅌ', 'ㅣ', '티', 'Tea / T-shirt', '티 나게 예쁜 오늘!'),
    ('ㅍ', 'ㅣ', '피', 'Blood', '피어나는 꽃처럼!'),
    ('ㅎ', 'ㅣ', '히', 'Hee (Laugh)', '히히, 신나는 하루!'),
]

def get_zone_info(day):
    if day <= 50:
        return "시즌 1: 당글마을의 탄생 (마을 광장, 따뜻한 봄빛)"
    elif day <= 120:
        return "시즌 2: 시끌벅적 저잣거리 (K-푸드와 시장, 한여름의 열기)"
    elif day <= 200:
        return "시즌 3: 미스터리 발음의 숲 (어려운 단어, 스산한 가을 단풍)"
    elif day <= 300:
        return "시즌 4: 바깥세상 미니어처 여행 (명소 투어, 겨울 눈꽃)"
    else:
        return "시즌 5: 대통합의 축제 (모두 모인 벚꽃 축제)"

with open('C:\\Users\\tuesv\\Documents\\DMDG_UT\\회의록\\025_dangeul_village_365_episodes.md', 'w', encoding='utf-8') as f:
    f.write('# 📅 [당글마을] 365일 쇼츠 에피소드 (테마파크 시즌 구조판)\n\n')
    f.write('**작성자**: 무라카미 하루키\n')
    f.write('**구조**: 1안(공간 기반 테마파크 구조) 및 사계절 질감 반영\n\n')
    f.write('| Day | 시즌 및 공간 (테마) | 자음 | 모음 | 완성 단어 | 에피소드 제목 (오늘의 단어) & 영어 뜻 |\n')
    f.write('|---|---|---|---|---|---|\n')
    
    current_zone = ""
    for i in range(1, 366):
        idx = (i - 1) % len(words_data)
        c, v, word, meaning, title = words_data[idx]
        
        zone_info = get_zone_info(i)
        if zone_info != current_zone:
            f.write(f'| **---** | **{zone_info}** | --- | --- | --- | --- |\n')
            current_zone = zone_info
            
        scenario = f"[당글마을 Day {i:03d}] 오늘의 단어: {word} ({meaning.split(' / ')[0]}) - {title}"
        f.write(f'| Day {i:03d} | {zone_info.split(":")[0]} | {c} | {v} | **{word}** | {scenario} |\n')

print("Generated 365 episodes with Season/Zone structure.")
