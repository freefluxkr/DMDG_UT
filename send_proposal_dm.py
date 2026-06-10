import os
import re
import json
import urllib.request
import urllib.parse
import time
from pathlib import Path
from PIL import Image
import io

# ── 설정 ─────────────────────────────────────
TOKEN   = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'

PROPOSAL_PATH = Path(r"c:\Users\tuesv\Documents\DMDG_UT\회의록\017_rainy_subway_shorts_proposal.md")
PORTRAITS_DIR = Path(r"c:\Users\tuesv\Documents\DMDG_UT\.agent\portraits")

# 에이전트 정보 매핑
AGENT_INFO = {
    '데미스': {'photo': 'demis.png', 'emoji': '👔', 'role': 'CEO/전략기획'},
    '하루키': {'photo': 'haruki.png', 'emoji': '✍️', 'role': '스토리/대본'},
    '무스타파': {'photo': 'mustafa.png', 'emoji': '🔬', 'role': '데이터/인프라'},
    '제니퍼': {'photo': 'jennifer.png', 'emoji': '🎨', 'role': '디자인'},
    '크레이그': {'photo': 'craig.png', 'emoji': '💻', 'role': '개발'},
    '짐머': {'photo': 'zimmer.png', 'emoji': '🎧', 'role': '사운드'},
    '사티아': {'photo': 'satya.png', 'emoji': '⚖️', 'role': '조직/평가'},
    '셜록': {'photo': 'sherlock.png', 'emoji': '🔍', 'role': '리서치/탐정'},
    '유피디': {'photo': 'upd.png', 'emoji': '📹', 'role': '유튜브 PD'}
}

def send_photo(chat_id, photo_path, caption):
    if not os.path.exists(photo_path):
        # 사진이 없으면 텍스트로 대체 전송
        url = f"{BASE_URL}/sendMessage"
        data = urllib.parse.urlencode({'chat_id': chat_id, 'text': caption, 'parse_mode': 'Markdown'}).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=15)
        return

    boundary = 'DMDGBoundary2026'
    try:
        with Image.open(photo_path) as img:
            new_size = (img.width // 4, img.height // 4)
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS)
            img_byte_arr = io.BytesIO()
            img_resized.save(img_byte_arr, format='PNG')
            file_data = img_byte_arr.getvalue()
    except Exception as e:
        print(f"이미지 리사이즈 실패: {e}")
        with open(photo_path, 'rb') as f:
            file_data = f.read()

    parts = []
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="profile.png"\r\nContent-Type: image/png\r\n\r\n'.encode())
    
    body = b''.join(parts) + file_data + f'\r\n--{boundary}--\r\n'.encode()
    
    req = urllib.request.Request(
        f'{BASE_URL}/sendPhoto', data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read())
            if res.get('ok'):
                print(f"전송 완료: {photo_path.name}")
            else:
                print(f"전송 실패(API 응답 오류): {res}")
    except Exception as e:
        print(f"전송 중 네트워크 오류: {e}")

def parse_and_send():
    if not PROPOSAL_PATH.exists():
        print(f"회의록 파일 없음: {PROPOSAL_PATH}")
        return

    with open(PROPOSAL_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 인물별 섹션 추출 (예: '## 👔 1. 데미스 (CEO) ...')
    pattern = r'(##\s+([^\n]+))\n(.*?)(?=\n##\s+|\Z)'
    sections = re.findall(pattern, content, re.DOTALL)

    print(f"총 {len(sections)}개의 섹션 파싱 완료. 전송을 시작합니다...")
    
    # 텔레그램 시작 메시지 전송
    init_url = f"{BASE_URL}/sendMessage"
    init_data = urllib.parse.urlencode({
        'chat_id': CHAT_ID,
        'text': "📢 *비서 페기 보고드립니다!*\n\n비 오는 날 지하철 매너 쇼츠 기획 및 신규 인프라 설계 회의 내용을 각 팀원들의 의견과 프로필 사진을 동봉해 보고합니다. 🌧️🚇",
        'parse_mode': 'Markdown'
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(init_url, data=init_data), timeout=15)
    time.sleep(1)

    for header, title, body in sections:
        # 타이틀에서 인물명 추출
        agent_name = None
        for key in AGENT_INFO.keys():
            if key in title:
                agent_name = key
                break
        
        if not agent_name:
            continue
            
        info = AGENT_INFO[agent_name]
        photo_path = PORTRAITS_DIR / info['photo']
        
        # 텔레그램 캡션 본문 편집 (마크다운 별표 없이 일반 텍스트 형태로 안전하게 전송)
        caption_text = f"[{info['emoji']} {agent_name} - {info['role']}]\n\n{body.strip()}"
        
        # 텔레그램 최대 캡션 제한(1024자) 방어
        if len(caption_text) > 1000:
            caption_text = caption_text[:990] + "..."
            
        print(f"발송 준비: {agent_name}")
        send_photo(CHAT_ID, photo_path, caption_text)
        
        # 과도한 동시 발송으로 인한 텔레그램 봇 API 제한(Rate limit) 방지용 딜레이
        time.sleep(1.5)

if __name__ == '__main__':
    parse_and_send()
