# 당목담글 (DMDG_UT) - 통합 프로젝트 백업

이 저장소는 **'사람과 마음을 연결하는 세상에서 가장 따뜻한 이어읽기 플랫폼'**인 당목담글 PWA 웹 애플리케이션과, 이를 홍보하기 위한 **30컷 수묵화 웹툰 렌더링 파이프라인**을 모두 포함하고 있는 통합 마스터 저장소입니다.

## 📂 디렉토리 구조 (Directory Structure)

```text
DMDG_UT/
├── .agent/                 # AI 에이전트(데미스, 사티아 등) 프로필, 인박스, 텔레그램 연동 설정
├── .venv/                  # 파이썬 가상환경 (의존성 패키지 7만여 개 포함)
├── AI_Knowledge_Base/      # 사내 AI / RAG 데이터베이스용 아카이브
├── IDEA/                   # 아이디어 스케치 및 기획 문서 보관
├── IMPL/                   # 구현체 및 아키텍처 관련 문서
├── RAG/                    # RAG(검색 증강 생성) 관련 데이터베이스 폴더
├── YOUTUBE/                # 유튜브 콘텐츠 제작 및 렌더링 파이프라인
│   ├── Projects/           # 개별 쇼츠/롱폼 프로젝트 영역
│   │   ├── Empress_Longform/       # 명성황후 롱폼 프로젝트
│   │   ├── Geumdeungjisa/          # 금등지사 쇼츠 프로젝트 (V3 파이프라인)
│   │   ├── JeongjoAssassination/   # 정조 암살 미수 사건 쇼츠 프로젝트
│   │   ├── SadoSeja/               # 사도세자 단독 에피소드 쇼츠 프로젝트
│   │   └── Subway_Shorts/          # 지하철 잔혹사 쇼츠 프로젝트
│   └── scripts/            # FFmpeg 및 Runway 등 자동화 파이썬 스크립트 모음
├── sodam-pwa/              # 당목담글 PWA 웹 애플리케이션 (React, Vite, Firebase)
│   ├── node_modules/       # npm 패키지 의존성 폴더 (대용량 파일 포함)
│   ├── public/             # 정적 리소스 파일
│   ├── src/                # 프론트엔드 핵심 소스 코드
│   └── (기타 설정 파일들)
├── 대화록/                 # AI 에이전트 및 팀 채팅 기록
├── 회의록/                 # 주요 의사결정 로그 백업
├── 봇_시작.bat             # 텔레그램 AI 에이전트 봇 실행 배치 파일
├── telegram_bot.py         # 텔레그램 봇 메인 실행 스크립트
├── test_ollama.py          # 로컬 AI 모델 연동 테스트 스크립트
└── (각종 시스템 관리 및 백업 .py / .bat 스크립트들)
```

### 주요 컴포넌트 요약
1. **`sodam-pwa/` (당목담글 PWA 웹앱)**
   - **기술 스택**: React, Vite, Firebase (Firestore & Hosting)
   - **주요 기능**: 브라우저 내장 마이크를 활용한 음성 녹음 및 랜덤 코르크 보드 형태의 '명예의 전당' UI.
   - **실행 방법**: `cd sodam-pwa` -> `npm install` -> `npm run dev`

2. **`YOUTUBE/` (유튜브 콘텐츠 파이프라인)**
   - **목적**: Runway Text-to-Video 통합, FFmpeg 오디오 믹싱(amix), 키네틱 자막 합성 등 쇼츠/롱폼 완전 자동화 렌더링.
   - 최근 **금등지사 V3 파이프라인**을 통해 수묵화 스타일 비주얼 생성 고도화 완료.

3. **`텔레그램 에이전트 연동` (`telegram_bot.py`, `.agent/`)**
   - **목적**: `TEAM_PROFILES.md`에 기반한 각 에이전트(데미스, 사티아 등)의 텔레그램 인박스 파일 전송 및 상태 관리.

## 🤖 AI Agents Team (마스터 & 어벤져스)
이 프로젝트는 인간 마스터(사장님)의 지휘 아래, 다음의 AI 에이전트들이 분업하여 구축되었습니다.
*   **Master**: 총괄 기획 및 최종 승인자 (사장님)
*   **Demis (CEO)**: 프로젝트 전략 수립, PWA 비즈니스 로직 및 전체 흐름 통제
*   **Peggy (Art Director)**: UI/UX 디자인, 수묵화풍 웹툰 프롬프트 엔지니어링 및 렌더링
*   **Mustafa (Infra)**: Firebase DB 구조화, Python 영상/오디오 파이프라인 아키텍처 설계 및 자동화 스크립트 작성

---
> **참고**: PWA 내부의 `node_modules`와 Python 임시 캐시 파일들은 `.gitignore`를 통해 업로드에서 제외되었습니다. 코드를 클론(Clone) 받은 후 반드시 `npm install` 등의 초기 세팅을 진행해주세요.

## 🔄 프로젝트 완전 복구 가이드 (PC 포맷 또는 Antigravity 재설치 시)

만약 PC를 포맷했거나 Antigravity를 완전히 새로 설치하여 **아무것도 없는 백지 상태**에서 시작해야 한다면, 아래의 단계를 순서대로 하나씩 따라와 주세요.

### 1단계: 필수 프로그램 설치 (사전 준비)
새 PC라면 먼저 아래 두 가지 프로그램이 설치되어 있어야 합니다.
1. **Git (버전 관리 프로그램)**: [https://git-scm.com/](https://git-scm.com/) 에서 다운로드 후 기본 설정으로 설치 (Next만 누르시면 됩니다).
2. **Node.js (웹앱 실행 환경)**: [https://nodejs.org/](https://nodejs.org/) 에서 **LTS 버전** 다운로드 후 설치.
3. (선택) **Python 3.10+**: 영상 합성(YOUTUBE 폴더) 작업을 이어가시려면 파이썬도 설치해야 합니다.

### 2단계: 소스코드 다운로드 (복구)
1. 윈도우 **명령 프롬프트(cmd)** 또는 **PowerShell**을 엽니다.
2. 코드를 저장하고 싶은 드라이브로 이동합니다. (예: D드라이브)
   ```cmd
   D:
   ```
3. 아래 명령어를 복사해서 붙여넣고 엔터를 치면 GitHub에서 전체 코드를 내려받습니다.
   ```cmd
   git clone https://github.com/freefluxkr/DMDG_UT.git
   ```
4. 명령어가 완료되면 `D:\DMDG_UT` 폴더가 생성됩니다.

### 3단계: Antigravity(AI 에이전트) 초기 세팅
1. Antigravity를 실행합니다.
2. 좌측 또는 설정 메뉴에서 **Workspace(작업 폴더)** 를 방금 다운로드 받은 **`D:\DMDG_UT`** 로 지정해 줍니다.
3. Antigravity 채팅창에 **아래 문장을 그대로 복사해서 붙여넣어 줍니다.** 이 주문을 통해 AI가 과거의 기억과 역할을 100% 되찾습니다.

> **[복구용 마법 주문]**
> "여기는 '당목담글(DMDG_UT)' 프로젝트 폴더야. 너는 지금부터 단순한 AI가 아니라 우리 팀의 AI 에이전트들이야.
> 먼저 최상단의 `README.md` 파일과 `회의록/` 폴더 안의 문서들(특히 팀 프로필과 스토리보드)을 전부 꼼꼼히 읽어줘.
> 다 읽은 후에는 현재 진행 상황을 요약해 주고, 너희들(Demis, Peggy, Mustafa)의 페르소나를 장착한 채로 나(Master)에게 앞으로 무엇을 하면 좋을지 보고해 줘. 
> PWA 앱과 YOUTUBE 렌더링 파이프라인 구조도 완벽히 파악해 줘."

### 4단계: PWA 웹앱(당목담글) 구동하기
소스코드만 다운받았을 뿐, 앱을 실행하기 위한 부품(라이브러리)들은 아직 없는 상태입니다. 아래 명령어로 부품을 조립하고 앱을 실행합니다.

1. Antigravity의 터미널(Terminal) 창을 엽니다.
2. 웹앱 폴더로 이동하여 패키지를 설치하고 실행합니다.
   ```bash
   cd D:\DMDG_UT\sodam-pwa
   npm install
   npm run dev
   ```
3. 화면에 나타난 `http://localhost:5173` 주소를 Ctrl 키를 누른 채로 클릭하면 브라우저에 당목담글 앱이 뜹니다.

### 5단계: 영상 합성 작업(YOUTUBE) 이어가기 (선택)
웹툰 컷 렌더링이나 영상 결합을 계속하시려면 파이썬 패키지를 설치해야 합니다.
```bash
cd D:\DMDG_UT\YOUTUBE
pip install -r requirements.txt  (의존성 파일이 없다면 opencv-python, gtts, moviepy 등을 수동 설치)
python render_video.py
```

### 💡 (팁) 작업 후 다시 백업하려면?
작업을 마친 뒤 변경된 내용을 다시 GitHub에 백업(저장)하려면 `D:\DMDG_UT` 최상단 폴더에서 다음 명령어들을 순서대로 실행하세요.
```bash
git add .
git commit -m "작업 내용 요약 적기"
git push
```
*(새 PC라면 처음 한 번은 GitHub 로그인 팝업이 뜰 수 있습니다.)*

---
## 🚀 2026-06-02 진행 상황 및 내일의 목표

# 당목담글 (DMDG_UT) - 통합 프로젝트 백업

이 저장소는 **'사람과 마음을 연결하는 세상에서 가장 따뜻한 이어읽기 플랫폼'**인 당목담글 PWA 웹 애플리케이션과, 이를 홍보하기 위한 **30컷 수묵화 웹툰 렌더링 파이프라인**을 모두 포함하고 있는 통합 마스터 저장소입니다.

## 📂 디렉토리 구조 (Directory Structure)

```text
DMDG_UT/
├── .agent/                 # AI 에이전트(데미스, 사티아 등) 프로필, 인박스, 텔레그램 연동 설정
├── .venv/                  # 파이썬 가상환경 (의존성 패키지 7만여 개 포함)
├── AI_Knowledge_Base/      # 사내 AI / RAG 데이터베이스용 아카이브
├── IDEA/                   # 아이디어 스케치 및 기획 문서 보관
├── IMPL/                   # 구현체 및 아키텍처 관련 문서
├── RAG/                    # RAG(검색 증강 생성) 관련 데이터베이스 폴더
├── YOUTUBE/                # 유튜브 콘텐츠 제작 및 렌더링 파이프라인
│   ├── Projects/           # 개별 쇼츠/롱폼 프로젝트 영역
│   │   ├── Empress_Longform/       # 명성황후 롱폼 프로젝트
│   │   ├── Geumdeungjisa/          # 금등지사 쇼츠 프로젝트 (V3 파이프라인)
│   │   ├── JeongjoAssassination/   # 정조 암살 미수 사건 쇼츠 프로젝트
│   │   ├── SadoSeja/               # 사도세자 단독 에피소드 쇼츠 프로젝트
│   │   └── Subway_Shorts/          # 지하철 잔혹사 쇼츠 프로젝트
│   └── scripts/            # FFmpeg 및 Runway 등 자동화 파이썬 스크립트 모음
├── sodam-pwa/              # 당목담글 PWA 웹 애플리케이션 (React, Vite, Firebase)
│   ├── node_modules/       # npm 패키지 의존성 폴더 (대용량 파일 포함)
│   ├── public/             # 정적 리소스 파일
│   ├── src/                # 프론트엔드 핵심 소스 코드
│   └── (기타 설정 파일들)
├── 대화록/                 # AI 에이전트 및 팀 채팅 기록
├── 회의록/                 # 주요 의사결정 로그 백업
├── 봇_시작.bat             # 텔레그램 AI 에이전트 봇 실행 배치 파일
├── telegram_bot.py         # 텔레그램 봇 메인 실행 스크립트
├── test_ollama.py          # 로컬 AI 모델 연동 테스트 스크립트
└── (각종 시스템 관리 및 백업 .py / .bat 스크립트들)
```

### 주요 컴포넌트 요약
1. **`sodam-pwa/` (당목담글 PWA 웹앱)**
   - **기술 스택**: React, Vite, Firebase (Firestore & Hosting)
   - **주요 기능**: 브라우저 내장 마이크를 활용한 음성 녹음 및 랜덤 코르크 보드 형태의 '명예의 전당' UI.
   - **실행 방법**: `cd sodam-pwa` -> `npm install` -> `npm run dev`

2. **`YOUTUBE/` (유튜브 콘텐츠 파이프라인)**
   - **목적**: Runway Text-to-Video 통합, FFmpeg 오디오 믹싱(amix), 키네틱 자막 합성 등 쇼츠/롱폼 완전 자동화 렌더링.
   - 최근 **금등지사 V3 파이프라인**을 통해 수묵화 스타일 비주얼 생성 고도화 완료.

3. **`텔레그램 에이전트 연동` (`telegram_bot.py`, `.agent/`)**
   - **목적**: `TEAM_PROFILES.md`에 기반한 각 에이전트(데미스, 사티아 등)의 텔레그램 인박스 파일 전송 및 상태 관리.

## 🤖 AI Agents Team (마스터 & 어벤져스)
이 프로젝트는 인간 마스터(사장님)의 지휘 아래, 다음의 AI 에이전트들이 분업하여 구축되었습니다.
*   **Master**: 총괄 기획 및 최종 승인자 (사장님)
*   **Demis (CEO)**: 프로젝트 전략 수립, PWA 비즈니스 로직 및 전체 흐름 통제
*   **Peggy (Art Director)**: UI/UX 디자인, 수묵화풍 웹툰 프롬프트 엔지니어링 및 렌더링
*   **Mustafa (Infra)**: Firebase DB 구조화, Python 영상/오디오 파이프라인 아키텍처 설계 및 자동화 스크립트 작성

---
> **참고**: PWA 내부의 `node_modules`와 Python 임시 캐시 파일들은 `.gitignore`를 통해 업로드에서 제외되었습니다. 코드를 클론(Clone) 받은 후 반드시 `npm install` 등의 초기 세팅을 진행해주세요.

## 🔄 프로젝트 완전 복구 가이드 (PC 포맷 또는 Antigravity 재설치 시)

만약 PC를 포맷했거나 Antigravity를 완전히 새로 설치하여 **아무것도 없는 백지 상태**에서 시작해야 한다면, 아래의 단계를 순서대로 하나씩 따라와 주세요.

### 1단계: 필수 프로그램 설치 (사전 준비)
새 PC라면 먼저 아래 두 가지 프로그램이 설치되어 있어야 합니다.
1. **Git (버전 관리 프로그램)**: [https://git-scm.com/](https://git-scm.com/) 에서 다운로드 후 기본 설정으로 설치 (Next만 누르시면 됩니다).
2. **Node.js (웹앱 실행 환경)**: [https://nodejs.org/](https://nodejs.org/) 에서 **LTS 버전** 다운로드 후 설치.
3. (선택) **Python 3.10+**: 영상 합성(YOUTUBE 폴더) 작업을 이어가시려면 파이썬도 설치해야 합니다.

### 2단계: 소스코드 다운로드 (복구)
1. 윈도우 **명령 프롬프트(cmd)** 또는 **PowerShell**을 엽니다.
2. 코드를 저장하고 싶은 드라이브로 이동합니다. (예: D드라이브)
   ```cmd
   D:
   ```
3. 아래 명령어를 복사해서 붙여넣고 엔터를 치면 GitHub에서 전체 코드를 내려받습니다.
   ```cmd
   git clone https://github.com/freefluxkr/DMDG_UT.git
   ```
4. 명령어가 완료되면 `D:\DMDG_UT` 폴더가 생성됩니다.

### 3단계: Antigravity(AI 에이전트) 초기 세팅
1. Antigravity를 실행합니다.
2. 좌측 또는 설정 메뉴에서 **Workspace(작업 폴더)** 를 방금 다운로드 받은 **`D:\DMDG_UT`** 로 지정해 줍니다.
3. Antigravity 채팅창에 **아래 문장을 그대로 복사해서 붙여넣어 줍니다.** 이 주문을 통해 AI가 과거의 기억과 역할을 100% 되찾습니다.

> **[복구용 마법 주문]**
> "여기는 '당목담글(DMDG_UT)' 프로젝트 폴더야. 너는 지금부터 단순한 AI가 아니라 우리 팀의 AI 에이전트들이야.
> 먼저 최상단의 `README.md` 파일과 `회의록/` 폴더 안의 문서들(특히 팀 프로필과 스토리보드)을 전부 꼼꼼히 읽어줘.
> 다 읽은 후에는 현재 진행 상황을 요약해 주고, 너희들(Demis, Peggy, Mustafa)의 페르소나를 장착한 채로 나(Master)에게 앞으로 무엇을 하면 좋을지 보고해 줘. 
> PWA 앱과 YOUTUBE 렌더링 파이프라인 구조도 완벽히 파악해 줘."

### 4단계: PWA 웹앱(당목담글) 구동하기
소스코드만 다운받았을 뿐, 앱을 실행하기 위한 부품(라이브러리)들은 아직 없는 상태입니다. 아래 명령어로 부품을 조립하고 앱을 실행합니다.

1. Antigravity의 터미널(Terminal) 창을 엽니다.
2. 웹앱 폴더로 이동하여 패키지를 설치하고 실행합니다.
   ```bash
   cd D:\DMDG_UT\sodam-pwa
   npm install
   npm run dev
   ```
3. 화면에 나타난 `http://localhost:5173` 주소를 Ctrl 키를 누른 채로 클릭하면 브라우저에 당목담글 앱이 뜹니다.

### 5단계: 영상 합성 작업(YOUTUBE) 이어가기 (선택)
웹툰 컷 렌더링이나 영상 결합을 계속하시려면 파이썬 패키지를 설치해야 합니다.
```bash
cd D:\DMDG_UT\YOUTUBE
pip install -r requirements.txt  (의존성 파일이 없다면 opencv-python, gtts, moviepy 등을 수동 설치)
python render_video.py
```

### 💡 (팁) 작업 후 다시 백업하려면?
작업을 마친 뒤 변경된 내용을 다시 GitHub에 백업(저장)하려면 `D:\DMDG_UT` 최상단 폴더에서 다음 명령어들을 순서대로 실행하세요.
```bash
git add .
git commit -m "작업 내용 요약 적기"
git push
```
*(새 PC라면 처음 한 번은 GitHub 로그인 팝업이 뜰 수 있습니다.)*

---
## 🚀 2026-06-02 진행 상황 및 내일의 목표

**[🔥 현재 100% 완벽하게 작동하는 최종 기능들 (HTML 시연 버전)]**
*   **화려한 디자인 복구**: 3D 문 뒤에 봄/가을/겨울 사진 쫘악~ 깔리고 거미줄 차트 완벽 출력!
*   **영령의 거울 (Gemini)**: 도슨트 제이 & 슬픈 영령들과의 소름 돋는 AI 대화!
*   **목소리 기부 & 엽서**: 목소리 감정 분석 후 Imagen 4.0 엽서까지 자동 생성!
*   **시공의 우체통 (Firebase 실시간 저장)**: 편지를 보내거나 낭독 기부를 완료하는 순간! 사장님의 Firebase 데이터베이스(Firestore)에 영구적으로 데이터가 꽂힙니다!

**[🛠️ 내일 진행할 작업 (전문가 모드)]**
*   **React(리액트) 정공법 리팩토링**: 현재 `museum-pwa/index.html` 단일 파일로 완성된 완벽한 로직을 바탕으로, 내일은 `museum-react` 폴더에서 본격적인 React 컴포넌트화 작업을 재개합니다.

---

## 🚨 [매우 중요] 퇴근 전 필수 Git 백업 가이드 (회사 PC)

집이나 다른 PC에서 원활하게 작업을 이어가려면, 퇴근하시기 전에 **반드시 현재 작업 내역을 인터넷(GitHub) 금고에 안전하게 100% 업로드(Push)** 해두셔야 합니다!

**VSCode의 터미널(Terminal) 창을 열고 아래 3줄의 명령어를 순서대로 쳐주세요!**

```bash
# 1. 오늘 작업한 모든 파일(변경된 파일 전체)을 백업 장바구니에 담습니다.
git add .

# 2. 백업 메모(라벨)를 적어서 장바구니를 꽉 묶어줍니다.
git commit -m "feat: 완벽한 HTML 시연 버전 완성 및 Firebase 연동 (React는 내일 진행)"

# 3. 묶은 장바구니를 인터넷(GitHub) 금고로 쏘아 올립니다! (제일 중요★)
git push
```
> **주의:** 마지막 `git push`를 쳤을 때 오류 없이 100% 게이지가 올라가며 업로드되어야 완료된 것입니다! (새 PC라면 로그인 팝업이 뜰 수 있습니다.)

---

## 🏠 집에서 이어서 작업하기 위한 가이드 (Home Workspace Guide)

집에 있는 다른 PC에서 이 작업을 그대로 이어가려면 아래 순서대로 진행해 주세요!

**1단계: 소스코드 다운로드 (Git Clone)**
집 PC의 원하는 폴더에서 터미널을 열고 코드를 내려받습니다.
```bash
git clone https://github.com/freefluxkr/DMDG_UT.git
```

**2단계: Antigravity(AI 에이전트) 깨우기 마법 주문**
Antigravity를 실행하고 작업 폴더(Workspace)를 방금 다운받은 `DMDG_UT` 폴더로 지정한 뒤, **아래 주문을 복사해서 AI 채팅창에 그대로 붙여넣어 주세요!**

> **[집에서 AI 팀원들 깨우기용 복사/붙여넣기 텍스트]**
> "안녕 팀원들! 집에서 다시 작업 시작이야! 
> 먼저 최상단의 `README.md` 파일과 `IDEA/implementation_plan.md` 파일을 읽고 우리가 어제 어디까지 했는지 완벽히 파악해 줘.
> 
> 어제 우리는 React 전환을 잠시 멈추고, `museum-pwa/index.html` 파일에 Firebase와 Gemini를 이식해서 '1차 HTML 시연 버전'을 완벽하게 성공시켰어. 
> 오늘 할 일은 어제 완성된 그 HTML의 로직들을 `museum-react` 폴더의 React(Vite) 프로젝트로 완벽하게 이식하는 '전문가 모드 리팩토링(Phase 3)'이야. 
> 준비되었으면 현재 상태를 요약하고 첫 번째 React 컴포넌트 이식 작업을 제안해 줘!"
