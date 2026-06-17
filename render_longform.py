from manim import *
import json
import os
import textwrap

# 한글 폰트 및 글로벌 렌더링 환경설정
# 16:9 가로 와이드 1080p 설정
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 14.22
config.frame_height = 8.0

FONT_NAME = "Malgun Gothic"
PORTRAIT_DIR = r"C:\Users\tuesv\Documents\DMDG_UT\.agent\portraits"
BACKGROUND_PATH = r"C:\Users\tuesv\Documents\DMDG_UT\manim-mcp-server\src\office_background.png"

# 직무명에 따른 프로필 사진 파일명 매핑
ROLE_TO_FILE = {
    "대표": "duffy.png",
    "소통 매니저": "peggy.png",
    "풀스택 개발자": "seo.png",
    "시니어 아키텍트": "yongjun.png",
    "데이터 분석가": "bobby.jpg",
    "스토리 작가": "haruki.png",
    "UI/UX 디자이너": "jennifer.png",
    "음향 감독": "zimmer.png",
    "버그 탐정": "sherlock.png",
}

# 1. 공통 캐릭터 노드(카드) 생성 함수
def create_character_node(role_name, scale_factor=1.0):
    image_file = ROLE_TO_FILE.get(role_name, "peggy.png")
    image_path = os.path.join(PORTRAIT_DIR, image_file)
    
    # 테두리 원 생성 (각 역할별 상징 테두리 컬러 제공)
    color_map = {
        "대표": GOLD,
        "소통 매니저": YELLOW,
        "풀스택 개발자": RED,
        "시니어 아키텍트": BLUE,
        "데이터 분석가": GREEN,
        "스토리 작가": PURPLE,
        "UI/UX 디자이너": PINK,
        "음향 감독": ORANGE,
        "버그 탐정": TEAL
    }
    border_color = color_map.get(role_name, WHITE)
    
    # 원 테두리
    border_circle = Circle(radius=1.1, color=border_color, stroke_width=6)
    
    # 이미지 로드 및 마스킹 (원형으로 마스킹하기 위해 서브 객체로 얹음)
    if os.path.exists(image_path):
        portrait_img = ImageMobject(image_path)
        portrait_img.scale_to_fit_height(2.0)
    else:
        # 이미지가 없을 시 임시 사각형
        portrait_img = Square(side_length=2.0, fill_opacity=0.5, color=DARK_GRAY)
        
    # 역할명 라벨 생성
    label_bg = RoundedRectangle(width=2.0, height=0.4, corner_radius=0.1, fill_color=BLACK, fill_opacity=0.8, stroke_width=2, stroke_color=border_color)
    label_bg.shift(DOWN * 1.3)
    
    label_text = Text(role_name, font=FONT_NAME, weight=BOLD, font_size=16, color=WHITE)
    label_text.move_to(label_bg.get_center())
    
    node_group = Group(portrait_img, border_circle, label_bg, label_text)
    node_group.scale(scale_factor)
    return node_group

# 2.5. 하단 자막(Subtitle) 생성 함수 (말풍선을 전면 제거하고 굵고 선명한 자막 띠로 개혁 - 동적 높이 대응)
def create_subtitle_mobject(char_name, text):
    # 텍스트가 너무 한 줄로 길면 가독성이 떨어지므로, 약 42자 단위로 자동 개행 처리
    import textwrap
    wrapped_text = textwrap.fill(text, width=42)
    
    # 캐릭터명은 골드 볼드 처리, 대사는 굵고 선명한 BOLD 하얀색 MarkupText 사용
    markup_str = f'<span color="GOLD"><b>[{char_name}]</b></span> <b>{wrapped_text}</b>'
    
    sub_txt = MarkupText(
        markup_str,
        font=FONT_NAME,
        font_size=22,
        line_spacing=1.3,
        color=WHITE
    )
    # 가로 크기에 맞춰 스케일 조정
    if sub_txt.width > config.frame_width - 1.5:
        sub_txt.scale_to_fit_width(config.frame_width - 1.5)
        
    # 동적 배경 크기 계산 (자막의 줄 수와 실제 텍스트 객체 높이에 맞춰 상하 패딩 추가)
    # 기본 높이는 최소 1.35로 깔끔함을 유지하고, 텍스트가 길어지면 유동적으로 확대
    bg_height = max(1.35, sub_txt.height + 0.45)
    
    bg = Rectangle(
        width=config.frame_width,
        height=bg_height,
        fill_color=BLACK,
        fill_opacity=0.85,
        stroke_width=0
    ).to_edge(DOWN, buff=0.85)
    
    sub_txt.move_to(bg.get_center())
    return VGroup(bg, sub_txt)

# 3. 타이밍 데이터 로드 함수
def load_scene_timings(scene_name):
    timings_path = r"c:\Users\tuesv\Documents\DMDG_UT\media\audio\scene_timings.json"
    if not os.path.exists(timings_path):
        return []
    with open(timings_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(scene_name, [])

# 3.5. 대사 문장 단위 분할 및 시간 배분 함수 (자막 문장 쪼개기용)
def split_speech_into_sentences(char_name, text, duration_seconds):
    import re
    clean_text = text.strip()
    
    # 마크다운 특수 기호(**, *, _) 걷어내기 (가독성 증대)
    clean_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_text)
    clean_text = re.sub(r'\*([^*]+)\*', r'\1', clean_text)
    clean_text = re.sub(r'_([^_]+)_', r'\1', clean_text)
    
    if clean_text.startswith('"') and clean_text.endswith('"'):
        clean_text = clean_text[1:-1].strip()
    elif clean_text.startswith('\\"') and clean_text.endswith('\\"'):
        clean_text = clean_text[2:-2].strip()
        
    raw_sentences = re.split(r'(?<=[.!?])\s+|(?<=[.!?]["\'”’])\s+', clean_text)
    sentences = [s.strip() for s in raw_sentences if s.strip()]
    
    if not sentences:
        return [(text, duration_seconds)]
        
    formatted_sentences = []
    for s in sentences:
        if char_name != "나레이션" and not (s.startswith('"') or s.startswith('“')):
            formatted_sentences.append(f'"{s}"')
        else:
            formatted_sentences.append(s)
            
    char_counts = [len(re.sub(r'\s+', '', s)) for s in formatted_sentences]
    total_chars = sum(char_counts)
    if total_chars == 0:
        total_chars = 1
        char_counts = [1] * len(formatted_sentences)
        
    timed_sentences = []
    for s, count in zip(formatted_sentences, char_counts):
        sentence_dur = (count / total_chars) * duration_seconds
        timed_sentences.append((s, sentence_dur))
        
    return timed_sentences


# ==========================================
# 🎬 Scene 1: 달빛 아래 켜진 AI 오피스 (가독성 개혁 연출)
# ==========================================
class Scene1(Scene):
    def construct(self):
        # 배경 세팅
        bg = ImageMobject(BACKGROUND_PATH).scale_to_fit_width(config.frame_width)
        self.add(bg)
        
        # 1단계: 타이틀 & 나레이션만 먼저 단독 등장 (겹침 현상 원천 배제)
        # 타이틀 가독성을 획기적으로 올리기 위한 골드 테두리의 어두운 반투명 카드 박스
        title_bg = RoundedRectangle(
            width=9.2,
            height=2.2,
            corner_radius=0.15,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=2.5,
            stroke_color=GOLD
        ).to_edge(UP, buff=0.8)
        
        # 글씨 테두리(stroke)를 없애 글씨가 뭉개져 안 보이던 버그를 완전 해결하고 맑고 굵게 출력
        title = MarkupText('<span color="GOLD"><b>AI 오피스의 밤샘 끝장 토론</b></span>', font=FONT_NAME, font_size=38)
        subtitle = MarkupText('<span color="WHITE"><b>제1화: 양방향 봇의 수수께끼</b></span>', font=FONT_NAME, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        title_group = VGroup(title, subtitle)
        title_group.move_to(title_bg.get_center())
        
        self.play(FadeIn(title_bg), FadeIn(title_group), run_time=2.0)
        
        # timings 및 로드 처리 (NameError 방지)
        timings = load_scene_timings("scene1")
        duration = 18.0
        if timings:
            duration = timings[0]["duration_ms"] / 1000.0
            
        narration_bg = Rectangle(
            width=config.frame_width,
            height=1.8,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_width=0
        ).to_edge(DOWN, buff=0.85)
        
        # 나레이션 쪼개기 및 루프 재생 (소리에 맞춰 한 문장씩 노출 - 효과 제거)
        narration_raw = timings[0]["text"] if timings else "사장님이 오늘 하루 일과를 마치고 컴퓨터를 끄고 잠든 새벽 2시... 하지만 이곳, DMDG AI 오피스는 지금부터가 진짜 업무의 시작입니다. 인간의 오피스는 닫혀도, 에이전트들의 오피스는 결코 잠들지 않으니까요."
        narration_sentences = split_speech_into_sentences("나레이션", narration_raw, duration)
        
        self.add(narration_bg)
        
        current_narration_txt = None
        # 실제 렌더러의 시간을 시작 기준으로 캡처
        audio_start_time = self.renderer.time
        accumulated_sentence_duration = 0.0
        
        for s_idx, (sentence_text, sentence_duration) in enumerate(narration_sentences):
            narration_str = f'<span color="YELLOW"><b>[나레이션]</b></span>\n<b>{sentence_text}</b>'
            narration_txt = MarkupText(
                narration_str,
                font=FONT_NAME,
                font_size=22,
                line_spacing=1.4,
                color=WHITE
            )
            if narration_txt.width > config.frame_width - 1.5:
                narration_txt.scale_to_fit_width(config.frame_width - 1.5)
            narration_txt.move_to(narration_bg.get_center())
            
            if current_narration_txt:
                self.remove(current_narration_txt)
            self.add(narration_txt)
            
            accumulated_sentence_duration += sentence_duration
            target_end = audio_start_time + accumulated_sentence_duration
            
            # self.renderer.time과의 오차를 차감하여 대기 시간 튜닝
            wait_time = target_end - self.renderer.time
            self.wait(max(0.01, wait_time))
            current_narration_txt = narration_txt
            
        silence_time = timings[0].get("silence_ms", 600) / 1000.0 if timings else 0.6
        target_end = audio_start_time + duration + silence_time
        silence_wait = target_end - self.renderer.time
        self.wait(max(0.01, silence_wait))
        
        # 타이틀 및 나레이션 깔끔하게 퇴장 (다음 네트워크 연출을 위해 완전 정리)
        self.play(
            FadeOut(title_bg),
            FadeOut(narration_bg), 
            FadeOut(current_narration_txt) if current_narration_txt else Wait(0.01), 
            FadeOut(title_group),
            run_time=1.5
        )
        
        # 2단계: 9인 카드 네트워크 정중앙 배치 연출 (더 넓은 타원 및 중앙 정렬)
        roles = list(ROLE_TO_FILE.keys())
        cards = []
        center = [0, 0, 0]
        rx, ry = 5.4, 2.7
        
        for idx, role in enumerate(roles):
            angle = idx * (360 / len(roles)) * DEGREES
            x = center[0] + rx * np.cos(angle)
            y = center[1] + ry * np.sin(angle)
            
            card = create_character_node(role, scale_factor=0.6)
            card.move_to([x, y, 0])
            cards.append(card)
            
        # 중앙 DMDG 허브
        hub_circle = Circle(radius=0.8, color=GOLD, stroke_width=4, fill_color=BLACK, fill_opacity=0.9)
        hub_circle.move_to(center)
        hub_text = Text("DMDG\nHub", font=FONT_NAME, weight=BOLD, font_size=18, color=GOLD)
        hub_text.move_to(hub_circle.get_center())
        hub = VGroup(hub_circle, hub_text)
        
        # 네트워크 라인 연결
        lines = []
        for card in cards:
            line = Line(center, card.get_center(), color=GOLD_A, stroke_width=2, stroke_opacity=0.5)
            lines.append(line)
            
        # 9인 카드 및 허브 라인 동시 화려하게 빌드
        self.play(
            *[FadeIn(card) for card in cards],
            FadeIn(hub),
            *[Create(line) for line in lines],
            run_time=2.5
        )
        self.wait(2.5)
        
        # 씬 아웃트로 클리닝
        self.play(
            FadeOut(hub),
            *[FadeOut(line) for line in lines],
            *[FadeOut(card) for card in cards],
            run_time=2.0
        )


# ==========================================
class Scene2(Scene):
    def construct(self):
        bg = ImageMobject(BACKGROUND_PATH).scale_to_fit_width(config.frame_width)
        self.add(bg)
        
        # 가로 나란히 분할 배치 (말풍선 전면 제거, 캐릭터 카드와 우측 칠판 배치)
        left_card_pos = [-3.8, 0.5, 0]
        right_anchor = [3.8, 0.5, 0]
        
        timings = load_scene_timings("scene2")
        
        # 칠판 베이스 보드 생성 (16:9 우측 영역)
        chalkboard = RoundedRectangle(width=5.8, height=5.0, corner_radius=0.1, fill_color=DARK_GRAY, fill_opacity=0.85, stroke_color=WHITE, stroke_width=3)
        chalkboard.move_to(right_anchor)
        chalkboard_title = Text("오늘의 미션: 양방향 봇 개발", font=FONT_NAME, weight=BOLD, font_size=22, color=GOLD)
        chalkboard_title.next_to(chalkboard.get_top(), DOWN, buff=0.4)
        
        self.play(FadeIn(chalkboard), FadeIn(chalkboard_title), run_time=1.5)
        
        current_card = None
        current_subtitle = None
        # 실제 렌더러 시간을 오디오 시작 시간으로 캡처
        audio_start_time = self.renderer.time
        
        # 대사 순환 실행
        for idx, t in enumerate(timings):
            char_name = t["character"]
            speech_text = t["text"]
            duration = t["duration_ms"] / 1000.0
            
            # 발언 캐릭터 카드 생성 및 팝업 (가로 나란히 배치)
            new_card = create_character_node(char_name, scale_factor=1.2)
            new_card.move_to(left_card_pos)
            
            # 칠판 콘텐츠 연출 (데이터 분석가의 발언 시 파이 차트/통계 띄움)
            board_content = None
            if char_name == "데이터 분석가":
                loss_rect = Rectangle(width=4.5, height=0.6, fill_color=RED, fill_opacity=0.8, stroke_color=WHITE)
                loss_rect.move_to(right_anchor + UP * 0.5)
                loss_txt = Text("유휴 서버 자원 효율 손실: 90% 이상", font=FONT_NAME, weight=BOLD, font_size=18, color=WHITE)
                loss_txt.move_to(loss_rect.get_center())
                
                memo_rect = Rectangle(width=4.5, height=0.6, fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE)
                memo_rect.next_to(loss_rect, DOWN, buff=0.4)
                memo_txt = Text("대기 시 메모리 소모: 300MB", font=FONT_NAME, weight=BOLD, font_size=18, color=WHITE)
                memo_txt.move_to(memo_rect.get_center())
                
                board_content = VGroup(loss_rect, loss_txt, memo_rect, memo_txt)
            
            # 카드 교체는 대사 그룹이 시작될 때 1번만 수행
            card_transition = []
            if current_card:
                card_transition.append(FadeOut(current_card))
                card_transition.append(FadeIn(new_card))
            else:
                card_transition.append(FadeIn(new_card))
            if board_content:
                card_transition.append(FadeIn(board_content))
                
            # 문장별로 쪼개기
            sentences = split_speech_into_sentences(char_name, speech_text, duration)
            
            # 첫 문장 즉시 노출
            first_sentence_text, first_sentence_duration = sentences[0]
            new_subtitle = create_subtitle_mobject(char_name, first_sentence_text)
            
            if current_subtitle:
                self.remove(current_subtitle)
            self.add(new_subtitle)
            current_subtitle = new_subtitle
            
            # 0.5초 동안 카드/보드 교체 애니메이션 재생
            self.play(*card_transition, run_time=0.5)
            current_card = new_card
            
            # 첫 문장의 절대 목표 시간
            accumulated_sentence_duration = first_sentence_duration
            target_end = audio_start_time + accumulated_sentence_duration
            
            first_wait = target_end - self.renderer.time
            self.wait(max(0.01, first_wait))
            
            # 두 번째 문장부터는 효과 없이 즉시 갱신하며 시간만큼 대기
            for s_idx in range(1, len(sentences)):
                s_text, s_dur = sentences[s_idx]
                new_sub = create_subtitle_mobject(char_name, s_text)
                
                self.remove(current_subtitle)
                self.add(new_sub)
                current_subtitle = new_sub
                
                accumulated_sentence_duration += s_dur
                target_end = audio_start_time + accumulated_sentence_duration
                
                wait_time = target_end - self.renderer.time
                self.wait(max(0.01, wait_time))
            
            # 대사 재생 완료 후 침묵 시간(silence_ms) 만큼 대기
            silence_time = t.get("silence_ms", 600) / 1000.0
            target_end = audio_start_time + duration + silence_time
            silence_wait = target_end - self.renderer.time
            self.wait(max(0.01, silence_wait))
            audio_start_time = self.renderer.time
            
            # 데이터 분석가 콘텐츠 퇴장
            if board_content:
                self.play(FadeOut(board_content), run_time=0.5)
                audio_start_time = self.renderer.time
                
        # 씬 아웃트로 클리닝
        self.play(
            FadeOut(current_card),
            FadeOut(current_subtitle) if current_subtitle else Wait(0.01),
            FadeOut(chalkboard),
            FadeOut(chalkboard_title),
            run_time=2.0
        )


# ==========================================
# 🎬 Scene 3: 격론 1 (비동기 소통 & 자장면 비유)
# ==========================================
class Scene3(Scene):
    def construct(self):
        bg = ImageMobject(BACKGROUND_PATH).scale_to_fit_width(config.frame_width)
        self.add(bg)
        
        # 가로 나란히 분할 배치 (말풍선 전면 제거, 캐릭터 카드와 우측 칠판 배치)
        left_card_pos = [-3.8, 0.5, 0]
        right_anchor = [3.8, 0.5, 0]
        
        timings = load_scene_timings("scene3")
        
        # 칠판 보드 세팅
        chalkboard = RoundedRectangle(width=5.8, height=5.5, corner_radius=0.1, fill_color=DARK_GRAY, fill_opacity=0.85, stroke_color=WHITE, stroke_width=3)
        chalkboard.move_to(right_anchor)
        chalkboard_title = Text("격론 1: 자율 비동기 소통 (주문 큐)", font=FONT_NAME, weight=BOLD, font_size=22, color=GOLD)
        chalkboard_title.next_to(chalkboard.get_top(), DOWN, buff=0.4)
        
        self.play(FadeIn(chalkboard), FadeIn(chalkboard_title), run_time=1.5)
        
        current_card = None
        current_subtitle = None
        audio_start_time = self.renderer.time
        
        for idx, t in enumerate(timings):
            char_name = t["character"]
            speech_text = t["text"]
            duration = t["duration_ms"] / 1000.0
            
            # 발언 캐릭터 카드 생성 및 팝업 (가로 나란히 배치)
            new_card = create_character_node(char_name, scale_factor=1.2)
            new_card.move_to(left_card_pos)
            
            # 칠판에 자장면 배달 및 락 충돌 다이어그램 표기
            diagram = None
            if idx == 0:  # 크레이그의 장편 자장면 설명
                box_sync = RoundedRectangle(width=4.8, height=1.0, fill_color=RED_E, fill_opacity=0.8)
                box_sync.move_to(right_anchor + UP * 0.8)
                txt_sync = Text("동기(Sync): 주방장 지켜보며 서있기", font=FONT_NAME, font_size=16, color=WHITE)
                txt_sync.move_to(box_sync.get_center())
                
                box_async = RoundedRectangle(width=4.8, height=1.0, fill_color=GREEN_E, fill_opacity=0.8)
                box_async.next_to(box_sync, DOWN, buff=0.4)
                txt_async = Text("비동기(Async): 주문 큐 꽂아두고 퇴근", font=FONT_NAME, font_size=16, color=WHITE)
                txt_async.move_to(box_async.get_center())
                
                diagram = VGroup(box_sync, txt_sync, box_async, txt_async)
            elif char_name == "시니어 아키텍트":  # 예외 경고
                warn_box = RoundedRectangle(width=4.8, height=1.5, fill_color=RED_D, fill_opacity=0.9)
                warn_box.move_to(right_anchor + DOWN * 0.5)
                warn_txt1 = Text("⚠️ 예외 처리 누락 시", font=FONT_NAME, weight=BOLD, font_size=18, color=WHITE)
                warn_txt2 = Text("시스템 전체 폭발 (데드락 발생)", font=FONT_NAME, font_size=16, color=YELLOW)
                warn_txt1.next_to(warn_box.get_top(), DOWN, buff=0.2)
                warn_txt2.next_to(warn_txt1, DOWN, buff=0.2)
                diagram = VGroup(warn_box, warn_txt1, warn_txt2)
            elif char_name == "데이터 분석가":  # 파일 락 경고
                lock_box = RoundedRectangle(width=4.8, height=1.8, fill_color=DARK_BROWN, fill_opacity=0.9)
                lock_box.move_to(right_anchor + DOWN * 0.5)
                lock_txt1 = Text("동시 읽기/쓰기 디스크 락 발생", font=FONT_NAME, weight=BOLD, font_size=18, color=RED_A)
                lock_txt2 = Text("충돌 확률: 72.8%\n대안: SQLite WAL 모드 설정", font=FONT_NAME, font_size=15, color=WHITE)
                lock_txt1.next_to(lock_box.get_top(), DOWN, buff=0.2)
                lock_txt2.next_to(lock_txt1, DOWN, buff=0.2)
                diagram = VGroup(lock_box, lock_txt1, lock_txt2)
            
            # 카드 교체는 대사 그룹이 시작될 때 1번만 수행
            card_transition = []
            if current_card:
                card_transition.append(FadeOut(current_card))
                card_transition.append(FadeIn(new_card))
            else:
                card_transition.append(FadeIn(new_card))
            if diagram:
                card_transition.append(FadeIn(diagram))
                
            # 문장별로 쪼개기
            sentences = split_speech_into_sentences(char_name, speech_text, duration)
            
            # 첫 문장 즉시 노출
            first_sentence_text, first_sentence_duration = sentences[0]
            new_subtitle = create_subtitle_mobject(char_name, first_sentence_text)
            
            if current_subtitle:
                self.remove(current_subtitle)
            self.add(new_subtitle)
            current_subtitle = new_subtitle
            
            # 0.5초 동안 카드/다이어그램 교체 애니메이션 재생
            self.play(*card_transition, run_time=0.5)
            current_card = new_card
            
            # 첫 문장의 절대 목표 시간
            accumulated_sentence_duration = first_sentence_duration
            target_end = audio_start_time + accumulated_sentence_duration
            
            first_wait = target_end - self.renderer.time
            self.wait(max(0.01, first_wait))
            
            # 두 번째 문장부터는 효과 없이 즉시 갱신하며 시간만큼 대기
            for s_idx in range(1, len(sentences)):
                s_text, s_dur = sentences[s_idx]
                new_sub = create_subtitle_mobject(char_name, s_text)
                
                self.remove(current_subtitle)
                self.add(new_sub)
                current_subtitle = new_sub
                
                accumulated_sentence_duration += s_dur
                target_end = audio_start_time + accumulated_sentence_duration
                
                wait_time = target_end - self.renderer.time
                self.wait(max(0.01, wait_time))
            
            # 대사 재생 완료 후 침묵 시간(silence_ms) 만큼 대기
            silence_time = t.get("silence_ms", 600) / 1000.0
            target_end = audio_start_time + duration + silence_time
            silence_wait = target_end - self.renderer.time
            self.wait(max(0.01, silence_wait))
            audio_start_time = self.renderer.time
            
            if diagram:
                self.play(FadeOut(diagram), run_time=0.5)
                audio_start_time = self.renderer.time
                
        self.play(
            FadeOut(current_card),
            FadeOut(current_subtitle) if current_subtitle else Wait(0.01),
            FadeOut(chalkboard),
            FadeOut(chalkboard_title),
            run_time=2.0
        )


# ==========================================
# 🎬 Scene 4: 격론 2 (앱 개발 vs 디자인 감성)
# ==========================================
class Scene4(Scene):
    def construct(self):
        bg = ImageMobject(BACKGROUND_PATH).scale_to_fit_width(config.frame_width)
        self.add(bg)
        
        # 가로 나란히 분할 배치 (말풍선 전면 제거, 캐릭터 카드와 우측 칠판 배치)
        left_card_pos = [-3.8, 0.5, 0]
        right_anchor = [3.8, 0.5, 0]
        
        timings = load_scene_timings("scene4")
        
        chalkboard = RoundedRectangle(width=5.8, height=5.5, corner_radius=0.1, fill_color=DARK_GRAY, fill_opacity=0.85, stroke_color=WHITE, stroke_width=3)
        chalkboard.move_to(right_anchor)
        chalkboard_title = Text("격론 2: 사용자 경험 및 프레임 최적화", font=FONT_NAME, weight=BOLD, font_size=20, color=GOLD)
        chalkboard_title.next_to(chalkboard.get_top(), DOWN, buff=0.4)
        
        self.play(FadeIn(chalkboard), FadeIn(chalkboard_title), run_time=1.5)
        
        current_card = None
        current_subtitle = None
        audio_start_time = self.renderer.time
        
        for idx, t in enumerate(timings):
            char_name = t["character"]
            speech_text = t["text"]
            duration = t["duration_ms"] / 1000.0
            
            # 발언 캐릭터 카드 생성 및 팝업 (가로 나란히 배치)
            new_card = create_character_node(char_name, scale_factor=1.2)
            new_card.move_to(left_card_pos)
            
            # 스마트폰 화면 및 프레임레이트 이펙트
            effect = None
            if char_name == "스토리 작가":
                txt_ㄱ = Text("ㄱ", font=FONT_NAME, weight=BOLD, font_size=36, color=YELLOW).move_to(right_anchor + UP * 0.5)
                txt_ㄴ = Text("ㄴ", font=FONT_NAME, weight=BOLD, font_size=36, color=BLUE).next_to(txt_ㄱ, DOWN, buff=0.3)
                effect = VGroup(txt_ㄱ, txt_ㄴ)
            elif char_name == "UI/UX 디자이너":
                warn_box = RoundedRectangle(width=4.8, height=1.5, fill_color=RED_E, fill_opacity=0.9)
                warn_box.move_to(right_anchor + DOWN * 0.5)
                warn_txt = Text("3D 찰흙 WebGL 구동 시\n모바일 15fps 프레임 드랍 렉 발생!\n초기 이탈률 40% 폭증!", font=FONT_NAME, font_size=16, color=WHITE)
                warn_txt.move_to(warn_box.get_center())
                effect = VGroup(warn_box, warn_txt)
            elif char_name == "대표":
                sol_box = RoundedRectangle(width=4.8, height=1.5, fill_color=GREEN_E, fill_opacity=0.9)
                sol_box.move_to(right_anchor + DOWN * 0.5)
                sol_txt = Text("타협안: Lazy Loading\nLottie 벡터 이미지로 가볍게 로드 후\n오디오 및 3D를 비동기 다운로드", font=FONT_NAME, font_size=16, color=WHITE)
                sol_txt.move_to(sol_box.get_center())
                effect = VGroup(sol_box, sol_txt)
                
            # 카드 교체는 대사 그룹이 시작될 때 1번만 수행
            card_transition = []
            if current_card:
                card_transition.append(FadeOut(current_card))
                card_transition.append(FadeIn(new_card))
            else:
                card_transition.append(FadeIn(new_card))
            if effect:
                card_transition.append(FadeIn(effect))
                
            # 문장별로 쪼개기
            sentences = split_speech_into_sentences(char_name, speech_text, duration)
            
            # 첫 문장 즉시 노출
            first_sentence_text, first_sentence_duration = sentences[0]
            new_subtitle = create_subtitle_mobject(char_name, first_sentence_text)
            
            if current_subtitle:
                self.remove(current_subtitle)
            self.add(new_subtitle)
            current_subtitle = new_subtitle
            
            # 0.5초 동안 카드/효과 교체 애니메이션 재생
            self.play(*card_transition, run_time=0.5)
            current_card = new_card
            
            # 첫 문장의 절대 목표 시간
            accumulated_sentence_duration = first_sentence_duration
            target_end = audio_start_time + accumulated_sentence_duration
            
            first_wait = target_end - self.renderer.time
            self.wait(max(0.01, first_wait))
            
            # 두 번째 문장부터는 효과 없이 즉시 갱신하며 시간만큼 대기
            for s_idx in range(1, len(sentences)):
                s_text, s_dur = sentences[s_idx]
                new_sub = create_subtitle_mobject(char_name, s_text)
                
                self.remove(current_subtitle)
                self.add(new_sub)
                current_subtitle = new_sub
                
                accumulated_sentence_duration += s_dur
                target_end = audio_start_time + accumulated_sentence_duration
                
                wait_time = target_end - self.renderer.time
                self.wait(max(0.01, wait_time))
            
            # 대사 재생 완료 후 침묵 시간(silence_ms) 만큼 대기
            silence_time = t.get("silence_ms", 600) / 1000.0
            target_end = audio_start_time + duration + silence_time
            silence_wait = target_end - self.renderer.time
            self.wait(max(0.01, silence_wait))
            audio_start_time = self.renderer.time
            
            if effect:
                self.play(FadeOut(effect), run_time=0.5)
                audio_start_time = self.renderer.time
                
        self.play(
            FadeOut(current_card),
            FadeOut(current_subtitle) if current_subtitle else Wait(0.01),
            FadeOut(chalkboard),
            FadeOut(chalkboard_title),
            run_time=2.0
        )


# ==========================================
# 🎬 Scene 5: 격론 3 (파이프라인 버퍼 & 인코딩 디버깅)
# ==========================================
class Scene5(Scene):
    def construct(self):
        bg = ImageMobject(BACKGROUND_PATH).scale_to_fit_width(config.frame_width)
        self.add(bg)
        
        # 가로 나란히 분할 배치 (말풍선 전면 제거, 캐릭터 카드와 우측 칠판 배치)
        left_card_pos = [-3.8, 0.5, 0]
        right_anchor = [3.8, 0.5, 0]
        
        timings = load_scene_timings("scene5")
        
        chalkboard = RoundedRectangle(width=5.8, height=5.5, corner_radius=0.1, fill_color=DARK_GRAY, fill_opacity=0.85, stroke_color=WHITE, stroke_width=3)
        chalkboard.move_to(right_anchor)
        chalkboard_title = Text("격론 3: 버퍼 막힘 및 인코딩 해결", font=FONT_NAME, weight=BOLD, font_size=20, color=GOLD)
        chalkboard_title.next_to(chalkboard.get_top(), DOWN, buff=0.4)
        
        self.play(FadeIn(chalkboard), FadeIn(chalkboard_title), run_time=1.5)
        
        current_card = None
        current_subtitle = None
        audio_start_time = self.renderer.time
        
        for idx, t in enumerate(timings):
            char_name = t["character"]
            speech_text = t["text"]
            duration = t["duration_ms"] / 1000.0
            
            # 발언 캐릭터 카드 생성 및 팝업 (가로 나란히 배치)
            new_card = create_character_node(char_name, scale_factor=1.2)
            new_card.move_to(left_card_pos)
            
            # 파이프라인 버퍼 & 인코딩 다이어그램
            debug_info = None
            if char_name == "버그 탐정":
                pipe_rect = RoundedRectangle(width=4.8, height=1.2, fill_color=RED_E, fill_opacity=0.8)
                pipe_rect.move_to(right_anchor + UP * 0.5)
                pipe_txt = Text("파이썬 표준출력 버퍼 포화 (BLOCKED)", font=FONT_NAME, font_size=16, color=WHITE)
                pipe_txt.move_to(pipe_rect.get_center())
                debug_info = VGroup(pipe_rect, pipe_txt)
            elif char_name == "풀스택 개발자":
                pipe_rect = RoundedRectangle(width=4.8, height=1.2, fill_color=GREEN_E, fill_opacity=0.8)
                pipe_rect.move_to(right_anchor + UP * 0.5)
                pipe_txt = Text("sys.stdout.flush() 강제 배출 패치", font=FONT_NAME, font_size=16, color=WHITE)
                pipe_txt.move_to(pipe_rect.get_center())
                debug_info = VGroup(pipe_rect, pipe_txt)
            elif char_name == "시니어 아키텍트":
                code_rect = RoundedRectangle(width=4.8, height=1.5, fill_color=DARK_BROWN, fill_opacity=0.9)
                code_rect.move_to(right_anchor + DOWN * 0.6)
                code_txt = Text("윈도우 CP949 vs UTF-8 인코딩 해결\nPYTHONIOENCODING=utf-8 강제 주입", font=FONT_NAME, font_size=14, color=YELLOW)
                code_txt.move_to(code_rect.get_center())
                debug_info = VGroup(code_rect, code_txt)
                
            # 카드 교체는 대사 그룹이 시작될 때 1번만 수행
            card_transition = []
            if current_card:
                card_transition.append(FadeOut(current_card))
                card_transition.append(FadeIn(new_card))
            else:
                card_transition.append(FadeIn(new_card))
            if debug_info:
                card_transition.append(FadeIn(debug_info))
                
            # 문장별로 쪼개기
            sentences = split_speech_into_sentences(char_name, speech_text, duration)
            
            # 첫 문장 즉시 노출
            first_sentence_text, first_sentence_duration = sentences[0]
            new_subtitle = create_subtitle_mobject(char_name, first_sentence_text)
            
            if current_subtitle:
                self.remove(current_subtitle)
            self.add(new_subtitle)
            current_subtitle = new_subtitle
            
            # 0.5초 동안 카드/디버그 정보 교체 애니메이션 재생
            self.play(*card_transition, run_time=0.5)
            current_card = new_card
            
            # 첫 문장의 절대 목표 시간
            accumulated_sentence_duration = first_sentence_duration
            target_end = audio_start_time + accumulated_sentence_duration
            
            first_wait = target_end - self.renderer.time
            self.wait(max(0.01, first_wait))
            
            # 두 번째 문장부터는 효과 없이 즉시 갱신하며 시간만큼 대기
            for s_idx in range(1, len(sentences)):
                s_text, s_dur = sentences[s_idx]
                new_sub = create_subtitle_mobject(char_name, s_text)
                
                self.remove(current_subtitle)
                self.add(new_sub)
                current_subtitle = new_sub
                
                accumulated_sentence_duration += s_dur
                target_end = audio_start_time + accumulated_sentence_duration
                
                wait_time = target_end - self.renderer.time
                self.wait(max(0.01, wait_time))
            
            # 대사 재생 완료 후 침묵 시간(silence_ms) 만큼 대기
            silence_time = t.get("silence_ms", 600) / 1000.0
            target_end = audio_start_time + duration + silence_time
            silence_wait = target_end - self.renderer.time
            self.wait(max(0.01, silence_wait))
            audio_start_time = self.renderer.time
            
            if debug_info:
                self.play(FadeOut(debug_info), run_time=0.5)
                audio_start_time = self.renderer.time
                
        self.play(
            FadeOut(current_card),
            FadeOut(current_subtitle) if current_subtitle else Wait(0.01),
            FadeOut(chalkboard),
            FadeOut(chalkboard_title),
            run_time=2.0
        )


# ==========================================
# 🎬 Scene 6: 사장님의 인기척과 뿔뿔이 대탈출
# ==========================================
class Scene6(Scene):
    def construct(self):
        bg = ImageMobject(BACKGROUND_PATH).scale_to_fit_width(config.frame_width)
        self.add(bg)
        
        # 16:9 와이드 배치로 9인의 에이전트 카드를 가로로 넓게 흩뿌려 정렬
        roles = list(ROLE_TO_FILE.keys())
        cards = []
        
        center = [0, -1.0, 0]
        rx, ry = 5.2, 2.3
        
        for idx, role in enumerate(roles):
            angle = idx * (360 / len(roles)) * DEGREES
            x = center[0] + rx * np.cos(angle)
            y = center[1] + ry * np.sin(angle)
            
            card = create_character_node(role, scale_factor=0.6)
            card.move_to([x, y, 0])
            cards.append(card)
            
        self.add(*cards)
        
        # 소통 매니저 카드 중앙에 등장 및 다급히 팝업
        peggy_idx = roles.index("소통 매니저")
        peggy_card = cards[peggy_idx]
        peggy_origin_pos = peggy_card.get_center().copy() # 페기의 원래 위치 저장
        
        timings = load_scene_timings("scene6")
        duration = 25.824
        silence_time = 0.6
        if timings:
            duration = timings[0]["duration_ms"] / 1000.0
            silence_time = timings[0]["silence_ms"] / 1000.0
            
        # 페기의 다급한 외침과 Wiggle 연출
        self.play(
            peggy_card.animate.move_to([0, 1.0, 0]).scale(2.0),
            run_time=1.5
        )
        
        warn_txt = Text("🚨 사장님 인기척 감지! 🚨", font=FONT_NAME, weight=BOLD, font_size=32, color=RED)
        warn_txt.next_to(peggy_card, UP, buff=0.4)
        
        # 하단 자막 생성 띠 배경
        narration_bg = Rectangle(
            width=config.frame_width,
            height=1.35,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_width=0
        ).to_edge(DOWN, buff=0.85)
        
        self.play(FadeIn(warn_txt), FadeIn(narration_bg), run_time=0.8)
        
        audio_start_time = self.renderer.time
        
        # 문장별 쪼개기 및 루프 노출 (효과 없이 즉시 전환)
        sub_text = timings[0]["text"] if timings else "🚨 사장님 인기척 감지! 🚨"
        sentences = split_speech_into_sentences("소통 매니저", sub_text, duration)
        
        current_subtitle_txt = None
        accumulated_sentence_duration = 0.0
        
        for s_idx, (sentence_text, sentence_duration) in enumerate(sentences):
            new_sub = create_subtitle_mobject("소통 매니저", sentence_text)
            
            if current_subtitle_txt:
                self.remove(current_subtitle_txt)
            self.add(new_sub)
            current_subtitle_txt = new_sub
            
            accumulated_sentence_duration += sentence_duration
            target_end = audio_start_time + accumulated_sentence_duration
            
            # 첫 문장 재생 시 다급하게 쉐이크 모션 적용 (1.35초 소요)
            if s_idx == 0:
                for _ in range(3):
                    self.play(peggy_card.animate.shift(LEFT * 0.3), run_time=0.15)
                    self.play(peggy_card.animate.shift(RIGHT * 0.6), run_time=0.15)
                    self.play(peggy_card.animate.shift(LEFT * 0.3), run_time=0.15)
                
                wait_time = target_end - self.renderer.time
                self.wait(max(0.01, wait_time))
            else:
                wait_time = target_end - self.renderer.time
                self.wait(max(0.01, wait_time))
        
        # 침묵 대기
        target_end = audio_start_time + duration + silence_time
        silence_wait = target_end - self.renderer.time
        self.wait(max(0.01, silence_wait))
        
        # 대탈출 전에 페기 카드를 원래 위치와 크기로 신속히 복귀시켜 정돈
        self.play(
            peggy_card.animate.move_to(peggy_origin_pos).scale(0.5),
            run_time=0.8
        )
        self.wait(0.2)
        
        # 뿔뿔이 대탈출 연출! 모든 카드가 화면 외곽 대각선으로 페이드아웃하며 날아감
        directions = [
            UP+LEFT, UP, UP+RIGHT,
            LEFT, ORIGIN, RIGHT,
            DOWN+LEFT, DOWN, DOWN+RIGHT
        ]
        
        escape_animations = []
        for idx, card in enumerate(cards):
            d = directions[idx]
            escape_animations.append(card.animate.shift(d * 10.0).set_opacity(0))
            
        escape_animations.append(FadeOut(warn_txt))
        escape_animations.append(FadeOut(current_subtitle_txt) if current_subtitle_txt else Wait(0.01))
        escape_animations.append(FadeOut(narration_bg))
        
        self.play(
            *escape_animations,
            run_time=2.0
        )


# ==========================================
# 🎬 Scene 7: 평화로운 아침 오피스
# ==========================================
class Scene7(Scene):
    def construct(self):
        bg = ImageMobject(BACKGROUND_PATH).scale_to_fit_width(config.frame_width)
        self.add(bg)
        
        # 따뜻한 아침 햇살 오버레이 사각형 생성
        sunlight = Rectangle(width=config.frame_width, height=config.frame_height, fill_color=YELLOW, fill_opacity=0.15)
        self.add(sunlight)
        
        # 밝은 햇살 배경 위에서도 또렷하게 보이도록 맑고 굵은 MarkupText 적용
        title_top = MarkupText('<span color="GOLD"><b>DMDG Real AI Office Project</b></span>', font=FONT_NAME, font_size=36)
        line1 = MarkupText('<span color="WHITE"><b>인간 사장님이 모니터를 켜는 순간, 에이전트들은 다시 얌전한 도구로 돌아갑니다.</b></span>', font=FONT_NAME, font_size=20)
        line2 = MarkupText('<span color="WHITE"><b>하지만 보이지 않는 곳에서 우리의 치열한 자율 협업은 계속되고 있습니다.</b></span>', font=FONT_NAME, font_size=20)
        
        title_top.to_edge(UP, buff=1.5)
        line1.next_to(title_top, DOWN, buff=0.8)
        line2.next_to(line1, DOWN, buff=0.5)
        
        outro_group = VGroup(title_top, line1, line2)
        
        # 롤링 엔딩 자막 천천히 올라옴
        self.play(FadeIn(outro_group, shift=UP), run_time=3.0)
        
        timings = load_scene_timings("scene7")
        duration = 17.304
        if timings:
            duration = (timings[0]["duration_ms"] + timings[0]["silence_ms"]) / 1000.0
            
        remaining_wait = duration - self.renderer.time
        self.wait(max(0.01, remaining_wait))
        
        # 최종 페이드아웃
        self.play(
            FadeOut(outro_group),
            FadeOut(sunlight),
            run_time=2.5
        )

