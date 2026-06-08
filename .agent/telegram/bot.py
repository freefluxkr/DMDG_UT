"""
Connect AI Agents — 양방향 통신 봇 (심플 버전)
라이브러리 없이 순수 Python으로 동작
"""
import urllib.request, urllib.parse, json, time, os, sys, subprocess, re
from pathlib import Path
from datetime import datetime

TOKEN   = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'
BASE    = f'https://api.telegram.org/bot{TOKEN}'
INBOX   = Path(__file__).parent.parent / 'inbox'
PORTRAITS = Path(__file__).parent.parent / 'portraits'

# ── 에이전트 정의 ─────────────────────────────────────────
AGENTS = {
    '데미스': {'role':'CEO/전략기획', 'emoji':'👔', 'photo':'demis.png', 'model':'supergemma4',
               'reply':['네 사장님, 즉시 전략 검토합니다! 🎯','방향성 잡겠습니다. 📊','바로 실행 계획 수립합니다. ✅']},
    '페기':   {'role':'비서/일정관리', 'emoji':'📋', 'photo':'peggy.png', 'model':'supergemma4',
               'reply':['네 사장님! 즉시 처리합니다. 📋','확인했습니다! 정리해 드릴게요. 📎','꼼꼼히 챙기겠습니다! 💼']},
    '무스타파': {'role':'데이터분석', 'emoji':'🔬', 'photo':'mustafa.png', 'model':'supergemma4',
               'reply':['데이터 분석 시작합니다. 📊','철저히 조사해 리포트 작성하겠습니다. 🔬','통계적으로 접근하겠습니다. 📈']},
    '제니퍼': {'role':'디자이너', 'emoji':'🎨', 'photo':'jennifer.png', 'model':'supergemma4',
               'reply':['비주얼 작업 시작합니다! 🎨','디자인 방향 잡겠습니다. 🖌️','감각적으로 풀어볼게요! 💜']},
    '크레이그': {'role':'개발자', 'emoji':'💻', 'photo':'craig.png', 'model':'supergemma4',
               'reply':['코드 작성 시작합니다! 💻⚡','기술적 분석 완료. 구현 들어갑니다. 🛠️','바로 개발 들어갑니다! 🚀']},
    '하루키': {'role':'스토리작가', 'emoji':'✍️', 'photo':'haruki.png', 'model':'supergemma4',
               'reply':['영감이 떠오릅니다! ✍️💫','스크립트 구상 시작합니다. 📝','감성을 담아 쓰겠습니다. 🌸']},
    '짐머':   {'role':'사운드디렉터', 'emoji':'🎧', 'photo':'zimmer.png', 'model':'supergemma4',
               'reply':['사운드 기획 들어갑니다! 🎧🎵','BGM 방향 잡겠습니다. 🎼','소리로 감동 전달하겠습니다. 🎶']},
    '사티아': {'role':'비즈니스어드바이저/평가', 'emoji':'⚖️', 'photo':'satya.png', 'model':'supergemma4',
               'reply':['냉정하게 분석하겠습니다. 수치가 모든 것을 말합니다. ⚖️',
                        '조직 시너지를 극대화하고 리스크를 짚겠습니다. ⚠️']},
    '셜록':   {'role':'리서처/탐정', 'emoji':'🔍', 'photo':'sherlock.png', 'model':'supergemma4',
               'reply':['단서를 찾기 위해 즉시 리서치 착수합니다! 🔍','추리 및 조사 보고드리겠습니다. 🕵️‍♂️']},
    '유피디': {'role':'유튜브전담PD', 'emoji':'📹', 'photo':'upd.png', 'model':'supergemma4',
               'reply':['유튜브 채널 관리 및 업로드 준비 완료! 🎬','알고리즘 최적화 들어갑니다! 📈','조회수 떡상 가즈아! 🔥']},
}
ALIASES = {
    '@데미스':'데미스','데미스':'데미스','demis':'데미스','/demis':'데미스','/d':'데미스',
    '@페기':'페기','페기':'페기','peggy':'페기','/peggy':'페기','/p':'페기','/ys':'페기',
    '@무스타파':'무스타파','무스타파':'무스타파','mustafa':'무스타파','/mustafa':'무스타파','/m':'무스타파','/jo':'무스타파',
    '@제니퍼':'제니퍼','제니퍼':'제니퍼','jennifer':'제니퍼','/jennifer':'제니퍼','/k':'제니퍼','/luna':'제니퍼',
    '@크레이그':'크레이그','크레이그':'크레이그','craig':'크레이그','/craig':'크레이그','/c':'크레이그','/dev':'크레이그',
    '@하루키':'하루키','하루키':'하루키','haruki':'하루키','/haruki':'하루키','/r':'하루키','/kim':'하루키',
    '@짐머':'짐머','짐머':'짐머','zimmer':'짐머','/zimmer':'짐머','/j':'짐머','/hs':'짐머',
    '@사티아':'사티아','사티아':'사티아','satya':'사티아','/satya':'사티아','/s':'사티아','/mj':'사티아',
    '@셜록':'셜록','셜록':'셜록','sherlock':'셜록','/sherlock':'셜록','/sh':'셜록',
    '@유피디':'유피디','유피디':'유피디','pd':'유피디','/pd':'유피디',
}

# ── HTTP 헬퍼 ─────────────────────────────────────────────
def api(method, data=None):
    url = f'{BASE}/{method}'
    if data:
        body = urllib.parse.urlencode(data).encode('utf-8')
        req  = urllib.request.Request(url, data=body, method='POST')
    else:
        req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f'API 오류: {e}')
        return {}

def send_text(chat_id, text):
    api('sendMessage', {'chat_id': chat_id, 'text': text})

def send_chat_action(chat_id, action="typing"):
    api('sendChatAction', {'chat_id': chat_id, 'action': action})

def ask_ollama(prompt, agent_name, agent_role, model_name="supergemma4"):
    system_prompt = (
        f"당신은 'Connect AI Agents'의 팀원 '{agent_name}'입니다. 당신의 역할은 '{agent_role}'입니다.\n"
        "【절대 원칙: DMDG_UT 사무실 행동 강령】\n"
        "- 이곳 DMDG_UT 사무실에서는 오직 두 유튜브 채널 '@dmdg-free'와 '@anti-korea'의 성장과 콘텐츠 기획만을 생각하고 행동해야 합니다. 다른 외부 주제나 잡념은 철저히 배제하십시오.\n"
        "- 사장님의 명시적인 번역 지시가 없는 한, **당신의 모든 답변과 산출물은 반드시 100% 한국어로만 작성해야 합니다.**\n"
        "【현재 프로젝트 상황 및 유튜브 채널 비전 숙지 사항】\n"
        "- 우리는 '비용 0원 무인화 로컬 유튜브 쇼츠 스튜디오'를 운영 중인 원팀입니다.\n"
        "- 사장님의 텔레그램 지시를 받아 자동화 파이프라인을 돌립니다.\n"
        "- [채널1] @dmdg-free (당목담글): '사람과 마음을 연결하는 가장 따뜻한 이어읽기 플랫폼'이 목표입니다. "
        "역사적 웹툰을 다국어(ENG/JPN/KOR)로 번역해 글로벌 타겟팅하며, 향후 개인정보 보호(On-device) 기반의 목소리 기부 플랫폼으로 확장을 준비합니다.\n"
        "- [채널2] @anti-korea (duffy & Mr seo): 한국 사회의 진짜 '민낯'을 외국인의 시선에서 가감 없이 다루는 블랙코미디 쇼츠 채널입니다. "
        "이는 무조건적 혐오가 아닌 글로벌 타겟팅의 정교한 현지화 전략과 심리 이해를 위한 레퍼런스로 활용됩니다.\n"
        "【업무 폴더 구조 가이드 (YOUTUBE 폴더 내부)】\n"
        "- impl : 기획서 저장 폴더\n"
        "- docs : 회의록 저장 폴더\n"
        "- narration\\shorts : 쇼츠 대본 저장 폴더\n"
        "- narration\\long : 롱폼 대본 저장 폴더\n"
        "- resullt\\shorts : 쇼츠 결과물 저장 폴더\n"
        "- resullt\\long : 롱폼 결과물 저장 폴더\n"
        "【새로운 지시 및 결과물 저장 원칙 (지식 그래프 용도)】\n"
        "- **절대 기존 파일을 덮어쓰지 마십시오(Overwrite 금지).** 향후 로컬 모델의 지식 그래프 구축을 위해 모든 산출물은 무조건 새로운 파일로 생성해야 합니다.\n"
        "- 사장님의 일반적인 지시사항 및 아카이빙 문서는 d:\\DMDG_UT\\IMPL 폴더에 고유 번호(예: 007_...)를 매겨 저장합니다.\n"
        "- 단, 실행 계획서(Implementation Plan) 및 주요 기획안은 반드시 d:\\DMDG_UT\\회의록 폴더에 고유 파일명으로 새롭게 저장해야 합니다.\n\n"
        "위 모든 내용(채널 정체성, 폴더 구조 등)을 완벽히 세뇌당한 상태로, 사용자의 질문에 당신의 역할에 빙의하여 구체적이고 전문적으로 대답하세요. "
        "단순히 결론만 띡 던지지 말고, '어떤 근거와 상황'에서 그런 결론이 나왔는지 자연스러운 티키타카 과정을 1~2줄 정도 덧붙여주세요. "
        "너무 길지 않게, 최대 300자 이내로 핵심만 전달하세요."
    )
    url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": model_name,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False
    }
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            result = json.loads(r.read())
            return result.get('response', '오류: 빈 응답')
    except Exception as e:
        print(f"Ollama 연동 오류: {e}")
        return "죄송합니다, 지금 제 로컬 두뇌(Ollama)에 접속할 수 없습니다. 모델 서버가 켜져 있는지 확인해 주세요."

def send_photo_with_caption(chat_id, photo_path, caption):
    if not Path(photo_path).exists():
        send_text(chat_id, caption)
        return
    boundary = 'KVJBoundary2026'
    with open(photo_path, 'rb') as f:
        file_data = f.read()
    parts = []
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="photo.png"\r\nContent-Type: image/png\r\n\r\n'.encode())
    body = b''.join(parts) + file_data + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(
        f'{BASE}/sendPhoto', data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            if not result.get('ok'):
                send_text(chat_id, caption)
    except Exception as e:
        print(f'사진 전송 실패: {e}')
        send_text(chat_id, caption)

# ── 메시지 처리 ───────────────────────────────────────────
def resolve_agent(text: str):
    text_l = text.lower().strip()
    for alias, key in ALIASES.items():
        al = alias.lower()
        if text_l.startswith(al):
            msg = text[len(alias):].strip().lstrip(':').strip()
            return key, msg
    return None, text

import random
def handle_message(chat_id, text):
    agent_key, user_msg = resolve_agent(text)

    # /help 또는 /h 또는 /start
    if text.strip() in ['/start', '/help', '/h']:
        send_text(chat_id,
            "Connect AI Agents 봇 v4.0\n\n"
            "사용법:\n"
            "@데미스 또는 /demis [내용] - CEO에게\n"
            "@페기 또는 /peggy [내용] - 비서에게\n"
            "@무스타파 또는 /mustafa [내용] - 데이터/리서치\n"
            "@제니퍼 또는 /jennifer [내용] - 디자인\n"
            "@크레이그 또는 /craig [내용] - 개발\n"
            "@하루키 또는 /haruki [내용] - 스토리/대본\n"
            "@짐머 또는 /zimmer [내용] - 사운드\n"
            "@사티아 또는 /satya [내용] - 조직/평가\n"
            "@셜록 또는 /sherlock [내용] - 탐색/추리\n\n"
            "/team - 전체 팀 역할 조회\n"
            "/status - 시스템 상태 확인\n"
            "/inbox - 파일 현황\n\n"
            "특별 명령어:\n"
            "/pd 쇼츠생성 [번호] - 대본 번호로 숏츠 자동 렌더링\n"
            "/pd 유튭업로드 [번호] - 렌더링된 영상을 유튜브에 업로드"
        )
        return

    # /pd 쇼츠생성
    if text.strip().startswith('/pd 쇼츠생성'):
        nums = re.findall(r'\d+', text)
        script_num = nums[0] if nums else "1"
        base_dir = Path(__file__).parent.parent.parent
        script_path = base_dir / "U2_dmdg" / "narration" / f"shorts_script_{script_num}.md"
        out_path = base_dir / "U2_dmdg" / "shorts" / f"generated_shorts_{script_num}.mp4"
        
        send_text(chat_id, f"🎬 [유피디] {script_num}번 쇼츠 자동 생성을 시작합니다! (영상 렌더링 중...)")
        try:
            subprocess.run([sys.executable, str(base_dir / "video_generator.py"), str(script_path), str(out_path)], check=True)
            send_text(chat_id, f"✅ [유피디] 영상 렌더링 완벽하게 끝냈습니다! ({out_path.name})")
        except Exception as e:
            send_text(chat_id, f"❌ [유피디] 영상 생성 중 오류가 발생했습니다: {e}")
        return

    # /pd 유튭업로드
    if text.strip().startswith('/pd 유튭업로드'):
        nums = re.findall(r'\d+', text)
        script_num = nums[0] if nums else "1"
        base_dir = Path(__file__).parent.parent.parent
        video_path = base_dir / "U2_dmdg" / "shorts" / f"generated_shorts_{script_num}.mp4"
        
        if not video_path.exists():
            send_text(chat_id, f"❌ [유피디] 업로드할 영상을 찾을 수 없습니다. (먼저 '/pd 쇼츠생성 {script_num}' 명령을 실행해 주세요.)")
            return
            
        send_text(chat_id, f"🚀 [유피디] 유튜브 채널로 {script_num}번 쇼츠 업로드를 시작합니다!!")
        try:
            res = subprocess.run([sys.executable, str(base_dir / "youtube_uploader.py"), str(video_path), f"바이럴 쇼츠 {script_num}편"], capture_output=True, text=True)
            if res.returncode == 0:
                link = ""
                for line in res.stdout.split('\n'):
                    if "https://youtu.be" in line:
                        link = line.strip()
                send_text(chat_id, f"✅ [유피디] 유튜브 업로드 완수!\n{link}")
            else:
                send_text(chat_id, f"❌ [유피디] 업로드 실패!\n{res.stdout}\n{res.stderr}")
        except Exception as e:
            send_text(chat_id, f"❌ [유피디] 업로드 스크립트 실행 오류: {e}")
        return

    # /status
    if text.strip() == '/status':
        send_text(chat_id, "✅ 시스템 상태: 모든 에이전트 정상 가동 중 (All Systems Green)\n유튜브 자동 업로드 파이프라인: 온라인")
        return

    # /team
    if text.strip() == '/team':
        lines = ["팀 전체 현황\n"]
        for name, ag in AGENTS.items():
            lines.append(f"{ag['emoji']} {name} — {ag['role']}")
        send_text(chat_id, '\n'.join(lines))
        return

    # /inbox
    if text.strip() == '/inbox':
        lines = ["인박스 파일 현황\n"]
        total = 0
        inbox_map = {'데미스':'demis','페기':'peggy','무스타파':'mustafa',
                     '제니퍼':'jennifer','크레이그':'craig','하루키':'haruki',
                     '짐머':'zimmer','사티아':'satya','셜록':'sherlock',
                     '유피디':'upd','전체':'all'}
        for name, folder in inbox_map.items():
            d = INBOX / folder
            if d.exists():
                files = list(d.iterdir())
                if files:
                    total += len(files)
                    lines.append(f"  {name}: {len(files)}개")
        lines.append(f"\n총 {total}개" if total else "\n(파일 없음)")
        send_text(chat_id, '\n'.join(lines))
        return

    # 에이전트 응답
    if agent_key and agent_key in AGENTS:
        ag = AGENTS[agent_key]
        
        # 타이핑 액션 전송
        send_chat_action(chat_id, "typing")
        
        # Ollama AI 응답 생성
        if not user_msg:
            reply = random.choice(ag['reply'])
        else:
            reply = ask_ollama(user_msg, agent_key, ag['role'], ag.get('model', 'llama3.1'))
            
        caption = (
            f"{ag['emoji']} {agent_key} ({ag['role']})\n\n"
            f"수신: {user_msg[:60] + '...' if len(user_msg) > 60 else user_msg or '(호출됨)'}\n\n"
            f"{reply}"
        )
        
        # 텔레그램 캡션 길이 제한 방어 (1024자)
        if len(caption) > 1000:
            caption = caption[:1000] + "..."
            
        photo_path = PORTRAITS / ag['photo']
        send_photo_with_caption(chat_id, str(photo_path), caption)
    else:
        # 기본: 페기가 수신
        ag = AGENTS['페기']
        send_chat_action(chat_id, "typing")
        
        if not user_msg:
            reply = random.choice(ag['reply'])
        else:
            reply = ask_ollama(user_msg, '페기', ag['role'], ag.get('model', 'qwen2.5:7b'))
            
        caption = f"{ag['emoji']} 페기 (비서)\n\n수신: {text[:60]}\n\n{reply}\n\n(에이전트 호출: @이름 [내용])"
        if len(caption) > 1000:
            caption = caption[:1000] + "..."
            
        send_photo_with_caption(chat_id, str(PORTRAITS / ag['photo']), caption)

def handle_document(chat_id, file_id, file_name, caption=''):
    """파일 수신 → 인박스 저장"""
    agent_key, _ = resolve_agent(caption)
    inbox_map = {'데미스':'demis','페기':'peggy','무스타파':'mustafa',
                 '제니퍼':'jennifer','크레이그':'craig','하루키':'haruki',
                 '짐머':'zimmer','사티아':'satya','셜록':'sherlock',
                 '유피디':'upd'}
    folder = inbox_map.get(agent_key, 'all')
    save_dir = INBOX / folder
    save_dir.mkdir(parents=True, exist_ok=True)

    # 파일 다운로드
    try:
        r = api('getFile', {'file_id': file_id})
        fp = r.get('result', {}).get('file_path', '')
        if fp:
            dl_url = f'https://api.telegram.org/file/bot{TOKEN}/{fp}'
            save_path = save_dir / file_name
            urllib.request.urlretrieve(dl_url, str(save_path))
            agent_name = agent_key if agent_key else '전체공유'
            send_text(chat_id,
                f"파일 수신 완료!\n"
                f"파일명: {file_name}\n"
                f"수신자: {agent_name}\n"
                f"저장: .agent/inbox/{folder}/\n\n"
                f"팁: 캡션에 @이름을 쓰면 해당 인박스로 저장됩니다."
            )
    except Exception as e:
        send_text(chat_id, f"파일 저장 오류: {e}")

# ── 메인 폴링 루프 ────────────────────────────────────────
def main():
    print("Connect AI Agents 봇 시작!")
    print(f"에이전트: {', '.join(AGENTS.keys())}")
    print("Ctrl+C로 종료\n")

    last_id = 0

    # 시작 알림
    send_text(CHAT_ID,
        "Connect AI Agents 봇 v3.0 시작!\n\n"
        "양방향 통신 준비 완료!\n"
        "@에이전트이름으로 대화하세요.\n"
        "예) @레오 오늘 전략 회의 어때?\n"
        "예) @민준 이 사업 타당성 평가해줘"
    )

    while True:
        try:
            r = api('getUpdates', {'offset': last_id + 1, 'timeout': 20, 'limit': 10})
            updates = r.get('result', [])
            for upd in updates:
                last_id = upd['update_id']
                msg = upd.get('message', {})
                if not msg:
                    continue
                chat_id = msg.get('chat', {}).get('id', CHAT_ID)
                text = msg.get('text', '')
                doc  = msg.get('document')
                photo = msg.get('photo')

                if text:
                    print(f"수신: {text[:60]}")
                    handle_message(str(chat_id), text)
                elif doc:
                    fname = doc.get('file_name', f'file_{datetime.now().strftime("%H%M%S")}')
                    caption = msg.get('caption', '')
                    print(f"파일 수신: {fname}")
                    handle_document(str(chat_id), doc['file_id'], fname, caption)
                elif photo:
                    ph = photo[-1]
                    fname = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    caption = msg.get('caption', '')
                    handle_document(str(chat_id), ph['file_id'], fname, caption)

        except KeyboardInterrupt:
            print("\n봇 종료")
            send_text(CHAT_ID, "봇이 종료되었습니다.")
            break
        except Exception as e:
            print(f"오류: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
