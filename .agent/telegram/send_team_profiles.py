"""팀 프로필 사진 + 정보를 텔레그램으로 순차 전송"""
import urllib.request, urllib.parse, json, sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOKEN   = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'
PORTRAIT_DIR = r'c:\Users\user\Downloads\connect_dmdg\.agent\portraits'

def send_text(msg):
    data = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': msg}).encode('utf-8')
    req  = urllib.request.Request(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        data=data, method='POST'
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read()).get('ok')

def send_photo(path, caption):
    import mimetypes
    boundary = '----FormBoundary7MA4YWxkTrZu0gW'
    with open(path, 'rb') as f:
        file_data = f.read()
    fname = os.path.basename(path)
    
    body  = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f'{CHAT_ID}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="caption"\r\n\r\n'
        f'{caption}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="photo"; filename="{fname}"\r\n'
        f'Content-Type: image/png\r\n\r\n'
    ).encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
    
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{TOKEN}/sendPhoto',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return result.get('ok')
    except Exception as e:
        print(f'  사진 전송 실패: {e}')
        return False

AGENTS = [
    ('leo.png',        '👔 레오 (Leo)\nCEO / 전략기획\n\n회사의 대표이자 전략가.\n빠른 판단력과 넓은 시야로 팀을 이끕니다.\n\n핵심 스킬: 전략기획 · 의사결정 · 투자유치 · 팀빌딩\n\n호출: @레오 또는 @leo'),
    ('youngsook.png',  '📋 영숙 (Youngsook)\n비서 / 일정관리\n\n꼼꼼하고 신속한 비서.\n일정, 문서, 커뮤니케이션을 완벽하게 관리합니다.\n\n핵심 스킬: 일정관리 · 문서정리 · 텔레그램보고 · 회의록\n\n호출: @영숙'),
    ('drjo.png',       '🔬 조박사 (Dr. Jo)\n데이터 분석 / 리서치\n\n데이터 기반 의사결정 전문가.\n시장 분석부터 AI 학습 데이터까지 깊이 파고듭니다.\n\n핵심 스킬: 데이터분석 · 시장조사 · 벤치마킹 · AI데이터\n\n호출: @조박사'),
    ('luna.png',       '🎨 루나 (Luna)\n디자이너 / UI/UX\n\n감각적인 비주얼 디자이너.\n색감과 레이아웃으로 브랜드 아이덴티티를 완성합니다.\n\n핵심 스킬: UI/UX · 브랜딩 · 일러스트 · 모션그래픽\n\n호출: @루나'),
    ('kodari.png',     '💻 코다리 (Kodari)\n개발자 / 풀스택\n\n전천후 풀스택 개발자.\n아이디어를 코드로 구현하는 핵심 엔진 역할.\n\n핵심 스킬: 풀스택개발 · Python · JavaScript · AI통합\n\n호출: @코다리'),
    ('writer_kim.png', '✍️ 김작가 (Writer Kim)\n스토리작가 / 스크립트\n\n감성 넘치는 스토리텔러.\n여행 나레이션부터 마케팅 카피까지 언어의 마법.\n\n핵심 스킬: 스크립트작성 · 나레이션 · 카피라이팅 · 스토리보드\n\n호출: @김작가'),
    ('hyunsoo.png',    '🎧 현수 (Hyunsoo)\n사운드 디렉터\n\n음악과 소리의 전문가.\nBGM, TTS 연출, 효과음으로 서비스에 생동감을 불어넣습니다.\n\n핵심 스킬: BGM제작 · TTS연출 · SFX디자인 · 음향믹싱\n\n호출: @현수'),
]

# 헤더 전송
send_text('👥 Connect AI Agents 팀 프로필 카드를 전송합니다!')
time.sleep(1)

for fname, caption in AGENTS:
    path = os.path.join(PORTRAIT_DIR, fname)
    if os.path.exists(path):
        ok = send_photo(path, caption)
        print(f'{"OK" if ok else "FAIL"}: {fname}')
    else:
        print(f'SKIP (없음): {fname}')
        send_text(caption)
    time.sleep(1.5)

# 마무리 안내
send_text(
    'Connect AI Agents 팀 구성 완료!\n\n'
    '텔레그램 봇 v3.0 업그레이드 내용:\n'
    '  /team - 전체 팀 조회\n'
    '  /profile [이름] - 개별 프로필+사진\n'
    '  /inbox - 파일 현황\n'
    '  /exec [명령] - 시스템 명령 실행\n'
    '  @이름 [내용] - 직접 대화\n'
    '  파일 전송 -> 자동 인박스 저장\n\n'
    '인박스: .agent/inbox/[직원이름]/\n'
    '사진: .agent/portraits/\n\n'
    '봇 실행: python .agent/telegram/bot.py'
)
print('완료!')
