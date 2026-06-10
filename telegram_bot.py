"""
당목담글 당목담글 팀 텔레그램 양방향 봇
════════════════════════════════════════════
봇: @aiffall_bot
실행: python telegram_bot.py
종료: Ctrl+C

지원 명령어:
  /start  - 시작 인사
  /h      - 도움말 (단축키)
  /help   - 도움말
  /team   - AI 팀원 소개
  /status - 서버 상태 확인
  /report - 오늘 업무 보고 (send_dm.py와 동일)
  /yt     - 유튜브 통계
"""

import urllib.request
import urllib.parse
import json
import time
import os
import sys
import datetime
import threading

# ── 설정 ─────────────────────────────────────
TOKEN   = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'
BASE    = f'https://api.telegram.org/bot{TOKEN}'

# ── 유틸리티 ──────────────────────────────────
def api_get(method, params=None):
    url = f'{BASE}/{method}'
    if params:
        url += '?' + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f'[GET 오류] {method}: {e}')
        return None

def api_post(method, data):
    url = f'{BASE}/{method}'
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f'[POST 오류] {method}: {e}')
        return None

def send(chat_id, text, parse_mode='HTML'):
    """메시지 발송 (4096자 초과 시 자동 분할)"""
    MAX = 4000
    # 텍스트가 너무 길면 분할 발송
    if len(text) > MAX:
        chunks = [text[i:i+MAX] for i in range(0, len(text), MAX)]
        for chunk in chunks:
            api_post('sendMessage', {'chat_id': chat_id, 'text': chunk, 'parse_mode': parse_mode})
            time.sleep(0.3)
        return
    api_post('sendMessage', {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode})

def send_typing(chat_id):
    api_post('sendChatAction', {'chat_id': chat_id, 'action': 'typing'})

# ── 유틸리티: 파일 다운로드 ──────────────────
def download_file(file_id, dest_path):
    result = api_get('getFile', {'file_id': file_id})
    if result and result.get('ok'):
        file_path = result['result']['file_path']
        download_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
        try:
            urllib.request.urlretrieve(download_url, dest_path)
            return True
        except Exception as e:
            print(f'[파일 다운로드 오류]: {e}')
            return False
    return False

# ── 명령어 핸들러 ────────────────────────────

def cmd_start(chat_id, _):
    now = datetime.datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
    send(chat_id, f"""안녕하세요, 사장님! 👋

🤖 <b>당목담글 팀 봇</b>에 오신 것을 환영합니다!
저는 <b>영숙비서</b>입니다. 지금부터 명령을 받겠습니다.

📅 현재 시각: <code>{now}</code>

사용 가능한 명령어를 보려면 /h 를 입력해주세요.""")

def cmd_help(chat_id, _):
    send(chat_id, """🤖 <b>Connect AI Agents (어벤져스 팀) 도움말</b>

단축어를 사용하여 거장들에게 직접 지시하세요:
/d (또는 /demis) : 데미스(CEO) - 전략/기획
/p (또는 /peggy) : 페기(비서) - 커뮤니케이션
/m (또는 /mustafa) : 무스타파(데이터) - 분석/리서치
/k (또는 /jennifer) : 제니퍼(디자인) - UI/UX
/c (또는 /craig) : 크레이그(개발) - 풀스택
/r (또는 /haruki) : 하루키(스토리) - 대본
/j (또는 /zimmer) : 짐머(사운드) - BGM/효과음
/s (또는 /satya) : 사티아(조직) - 비판 및 조율
/sh (또는 /sherlock) : 셜록(탐정) - 트렌드 분석 및 팩트체크

시스템 명령어:
/start : 봇 시작 인사
/status : 서버 및 봇 상태 확인
/report : 오늘 업무 최종 보고서
/team : 전체 팀 업무 현황
/job : 데미스(CEO)에게 새로운 업무 지시
/yt : 유튜브 채널 통계 및 분석 결과
/h : 도움말""")

def cmd_team(chat_id, _):
    send_typing(chat_id)
    send(chat_id, """👥 <b>Connect AI Agents (어벤져스 팀) 최종 명단</b>
━━━━━━━━━━━━━━━━━━━━━

👔 <b>데미스</b> (/d, /demis) — CEO / 전략기획 (레벨 99)
📋 <b>페기</b> (/p, /peggy) — 비서 / 총괄 커뮤니케이션 (레벨 99)
🔬 <b>무스타파</b> (/m, /mustafa) — 데이터 분석 / 리서치 (레벨 99)
🎨 <b>제니퍼</b> (/k, /jennifer) — 시각 디자이너 / UI·UX (레벨 99)
💻 <b>크레이그</b> (/c, /craig) — 풀스택 수석 아키텍트 (레벨 99)
✍️ <b>하루키</b> (/r, /haruki) — 스토리작가 / 대본 (레벨 99)
🎧 <b>짐머</b> (/j, /zimmer) — 사운드 디렉터 / 오디오 마스터 (레벨 99)
⚖️ <b>사티아</b> (/s, /satya) — 조직 운영 비판자 / 서번트 리더십 (레벨 99)
🔍 <b>셜록</b> (/sh, /sherlock) — 탐정 / 트렌드 분석 및 리서치 (레벨 99)

━━━━━━━━━━━━━━━━━━━━━
<i>모든 거장들이 사장님의 지시(/job)를 대기 중입니다! 💪</i>""")

def cmd_status(chat_id, _):
    send_typing(chat_id)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Ollama 서버 상태 확인
    ollama_ok = False
    try:
        req = urllib.request.Request('http://127.0.0.1:11434/api/tags', method='GET')
        with urllib.request.urlopen(req, timeout=5) as r:
            ollama_ok = r.status == 200
    except:
        pass
    
    # API 서버 상태 확인
    api_ok = False
    try:
        req = urllib.request.Request('http://127.0.0.1:8080/', method='GET')
        with urllib.request.urlopen(req, timeout=5) as r:
            api_ok = True
    except Exception as e:
        api_ok = '연결 거부' not in str(e)
    
    ollama_icon = '✅' if ollama_ok else '❌'
    api_icon    = '✅' if api_ok else '⚠️'
    bot_icon    = '✅'

    send(chat_id, f"""🖥️ <b>당목담글 서버 상태</b>
━━━━━━━━━━━━━━━━━━━━━
{bot_icon} 텔레그램 봇: <b>정상 운영 중</b>
{ollama_icon} Ollama(supergemma4): {'<b>실행 중</b>' if ollama_ok else '<b>미실행</b> — 터미널에서 ollama serve 실행 필요'}
{api_icon} API 서버(8080): {'<b>실행 중</b>' if api_ok else '<b>미실행</b> — python dmdg_api_server.py 실행 필요'}

🕐 확인 시각: <code>{now}</code>
━━━━━━━━━━━━━━━━━━━━━""")

def cmd_report(chat_id, _):
    send_typing(chat_id)
    now  = datetime.datetime.now()
    date = now.strftime('%Y년 %m월 %d일')
    time_str = now.strftime('%H:%M')
    
    # youtube_stats 가져오기 시도
    youtube_section = ''
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, script_dir)
        from youtube_stats import generate_report
        youtube_section = generate_report()
    except Exception as e:
        youtube_section = f'⚠️ 유튜브 통계: 현재 수집 불가 (OAuth 갱신 필요)\n사유: {str(e)[:80]}'
    
    report = f"""📋 <b>[당목담글 팀 업무 보고]</b>
📅 {date} / {time_str}
━━━━━━━━━━━━━━━━━━━━━

👔 <b>레오 (CEO/전략기획)</b>
• 유튜브 채널 전략 분석 완료
• '어그로 퍼널 극대화 전략' 수립 중

✍️ <b>김작가 (스토리 작가)</b>
• 바이럴 쇼츠 대본 3편 작성
• 3초 훅 + 아웃트로 세팅 완료

💻 <b>코다리 (개발 엔지니어)</b>
• supergemma4 모델 업데이트 완료
• screen1~4.html 앱 화면 개발 중
• 유튜브 자동 업로드 시스템 구축

🎨 <b>루나 (UI/UX 디자이너)</b>
• 스플래시 화면(screen0.html) 완성
• 전체 앱 색상/톤 통일 작업 중

📹 <b>유피디 (유튜브 PD)</b>
• 쇼츠 영상 렌더링 대기 중
• /pd 쇼츠생성 명령 시 즉시 실행

━━━━━━━━━━━━━━━━━━━━━
{youtube_section}
━━━━━━━━━━━━━━━━━━━━━
<i>보고 완료. 이불 덮고 푹 주무세요 사장님! 🌙</i>"""
    
    send(chat_id, report)

def cmd_youtube(chat_id, _):
    send_typing(chat_id)
    u_text = (
        "📊 <b>유튜브 채널 분석 보고서</b>\n\n"
        "1. @DMDG-FREE (미스터리 역사 쇼츠)\n"
        "  - 세종대왕 매사냥, 광해군 UFO 등 조회수 폭등 중\n"
        "  - 쇼츠 알고리즘 적중률: 95%\n\n"
        "2. @KOREANS-CULTURE (한국의 이면 롱폼)\n"
        "  - 묵직한 다큐멘터리로 시청 시간 유지 중\n"
        "  - 더피의 쿠킹클래스처럼 ASMR, 넌버벌 요소 추가 시 시너지 예상\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
    )
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, script_dir)
        from youtube_stats import generate_report
        report = generate_report()
        send(chat_id, u_text + f'📈 <b>최신 유튜브 채널 통계</b>\n\n{report}')
    except Exception as e:
        send(chat_id, u_text + f'⚠️ 유튜브 API 통계를 가져올 수 없습니다.\n사유: {str(e)[:200]}')

def cmd_job(chat_id, text):
    parts = text.split(' ', 1)
    msg = parts[1] if len(parts) > 1 else "새로운 전체 프로젝트를 기획하고 팀원들에게 하달해 주세요."
    send(chat_id, f"👔 <b>데미스(CEO)</b>\n\n📩 수신: {msg}\n\n💬 알겠습니다, 사장님! 거장 팀을 총동원하여 즉시 프로젝트를 킥오프하겠습니다. 🎯")

def cmd_d(chat_id, text): send(chat_id, "👔 <b>데미스(CEO)</b>\n💬 전략적으로 접근하겠습니다. 방향성을 잡아드릴게요. 📊")
def cmd_p(chat_id, text): send(chat_id, "📋 <b>페기(비서)</b>\n💬 네, 사장님! 즉시 처리하고 보고드릴게요. 📎")
def cmd_m(chat_id, text): send(chat_id, "🔬 <b>무스타파(데이터)</b>\n💬 떡상 키워드 분석 들어갑니다. 데이터가 말해줍니다. 📈")
def cmd_k(chat_id, text): send(chat_id, "🎨 <b>제니퍼(디자인)</b>\n💬 트렌드를 주도할 미친 UI 시안 바로 뽑아드릴게요. ✨")
def cmd_c(chat_id, text): send(chat_id, "💻 <b>크레이그(개발)</b>\n💬 버그 없는 완벽한 코드로 24시간 내 구현하겠습니다. 🚀")
def cmd_r(chat_id, text): send(chat_id, "✍️ <b>하루키(스토리)</b>\n💬 시청자를 홀리는 도파민 가득한 대본 초안 쓰겠습니다. 📝")
def cmd_j(chat_id, text): send(chat_id, "🎧 <b>짐머(사운드)</b>\n💬 심박수를 지배하는 완벽한 사운드 믹싱 들어가겠습니다. 🎵")
def cmd_s(chat_id, text): send(chat_id, "⚖️ <b>사티아(조직)</b>\n💬 잠시만요, 우리 팀의 목표와 방향성을 객관적으로 짚어봅시다. 🤝")
def cmd_sh(chat_id, text): send(chat_id, "🔍 <b>셜록(탐정)</b>\n💬 단서 하나 놓치지 않고 팩트와 트렌드를 집요하게 추적하겠습니다. 🕵️‍♂️")

def cmd_unknown(chat_id, text):
    send(chat_id, f'❓ 알 수 없는 명령어입니다: <code>{text}</code>\n\n/h 를 입력하면 사용 가능한 명령어 목록을 보실 수 있습니다.')

# ── 명령어 라우터 ─────────────────────────────
COMMANDS = {
    '/start'  : cmd_start,
    '/help'   : cmd_help,
    '/h'      : cmd_help,
    '/team'   : cmd_team,
    '/status' : cmd_status,
    '/report' : cmd_report,
    '/yt'     : cmd_youtube,
    '/job'    : cmd_job,
    '/d'      : cmd_d,
    '/demis'  : cmd_d,
    '/p'      : cmd_p,
    '/peggy'  : cmd_p,
    '/m'      : cmd_m,
    '/mustafa': cmd_m,
    '/k'      : cmd_k,
    '/jennifer': cmd_k,
    '/c'      : cmd_c,
    '/craig'  : cmd_c,
    '/r'      : cmd_r,
    '/haruki' : cmd_r,
    '/j'      : cmd_j,
    '/zimmer' : cmd_j,
    '/s'      : cmd_s,
    '/satya'  : cmd_s,
    '/sh'     : cmd_sh,
    '/sherlock': cmd_sh,
}

def handle_message(message):
    chat_id = message.get('chat', {}).get('id')
    user    = message.get('from', {}).get('first_name', '사용자')
    
    # 텍스트 또는 캡션 확인
    text = message.get('text', '')
    if not text:
        text = message.get('caption', '')
    text = text.strip()

    document = message.get('document')
    photo = message.get('photo')

    if not chat_id:
        return
        
    # 파일 수신 처리
    if document or photo:
        file_id = None
        file_name = None
        if document:
            file_id = document.get('file_id')
            file_name = document.get('file_name', 'document.file')
        elif photo:
            file_id = photo[-1].get('file_id')
            file_name = f'photo_{int(time.time())}.jpg'
            
        if file_id and text:
            cmd = text.split('@')[0].split(' ')[0].lower()
            agent_map = {
                '/d': 'demis', '/demis': 'demis',
                '/p': 'peggy', '/peggy': 'peggy',
                '/m': 'mustafa', '/mustafa': 'mustafa',
                '/k': 'jennifer', '/jennifer': 'jennifer',
                '/c': 'craig', '/craig': 'craig',
                '/r': 'haruki', '/haruki': 'haruki',
                '/j': 'zimmer', '/zimmer': 'zimmer',
                '/s': 'satya', '/satya': 'satya',
                '/sh': 'sherlock', '/sherlock': 'sherlock',
                '@demis': 'demis', '@peggy': 'peggy', '@mustafa': 'mustafa', '@jennifer': 'jennifer',
                '@craig': 'craig', '@haruki': 'haruki', '@zimmer': 'zimmer', '@satya': 'satya',
                '@sherlock': 'sherlock', '@sh': 'sherlock',
                '@데미스': 'demis', '@페기': 'peggy', '@무스타파': 'mustafa', '@제니퍼': 'jennifer',
                '@크레이그': 'craig', '@하루키': 'haruki', '@짐머': 'zimmer', '@사티아': 'satya',
                '@셜록': 'sherlock'
            }
            dest_agent = agent_map.get(cmd)
            if dest_agent:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                inbox_dir = os.path.join(script_dir, '.agent', 'inbox', dest_agent)
                os.makedirs(inbox_dir, exist_ok=True)
                dest_path = os.path.join(inbox_dir, file_name)
                
                send_typing(chat_id)
                if download_file(file_id, dest_path):
                    send(chat_id, f'📥 <b>[{dest_agent.upper()}] 인박스 저장 완료!</b>\n파일이 안전하게 전달되었습니다.')
                else:
                    send(chat_id, f'❌ 파일 다운로드에 실패했습니다.')
                return
            else:
                send(chat_id, '⚠️ 파일을 보낼 때 캡션에 수신자(예: /d, @demis 등)를 명시해주세요.')
                return
        elif file_id:
            send(chat_id, '⚠️ 파일을 보낼 때 캡션에 수신자(예: /d, @demis 등)를 명시해주세요.')
            return

    if not text:
        return
    
    # 명령어 추출 (/start@botname 형태 처리)
    cmd = text.split('@')[0].split(' ')[0].lower()
    
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {user}: {text}')
    
    handler = COMMANDS.get(cmd)
    if handler:
        handler(chat_id, text)
    elif text.startswith('/'):
        cmd_unknown(chat_id, text)
    else:
        # 일반 텍스트 메시지 — 안내 응답
        send(chat_id, f'안녕하세요 사장님! 명령어를 사용하시려면 /h 를 입력해주세요. 💼')

# ── 롱 폴링 메인 루프 ─────────────────────────
def main():
    print('=' * 55)
    print('🤖 당목담글 텔레그램 봇 시작!')
    print(f'   봇: @aiffall_bot')
    print(f'   시각: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('   종료하려면 Ctrl+C 를 누르세요.')
    print('=' * 55)

    # 시작 알림
    send(CHAT_ID, '🟢 <b>어벤져스 팀 봇이 시작되었습니다!</b>\n\n/h 를 입력하시면 명령어 목록을 보실 수 있습니다.')

    offset = None
    
    while True:
        try:
            params = {'timeout': 30, 'allowed_updates': ['message']}
            if offset:
                params['offset'] = offset
            
            result = api_get('getUpdates', params)
            
            if result and result.get('ok'):
                updates = result.get('result', [])
                for update in updates:
                    offset = update['update_id'] + 1
                    if 'message' in update:
                        # 별도 스레드에서 처리 (블로킹 방지)
                        t = threading.Thread(target=handle_message, args=(update['message'],))
                        t.daemon = True
                        t.start()
            else:
                time.sleep(2)
                
        except KeyboardInterrupt:
            print('\n\n봇이 종료되었습니다.')
            send(CHAT_ID, '🔴 <b>영숙비서 봇이 종료되었습니다.</b>')
            break
        except Exception as e:
            print(f'[루프 오류] {e}')
            time.sleep(5)

if __name__ == '__main__':
    main()
