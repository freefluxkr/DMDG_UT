# 당목담글 (DMDG_UT) - 통합 프로젝트 백업

이 저장소는 **'사람과 마음을 연결하는 세상에서 가장 따뜻한 이어읽기 플랫폼'**인 당목담글 PWA 웹 애플리케이션과, 이를 홍보하기 위한 **30컷 수묵화 웹툰 렌더링 파이프라인**을 모두 포함하고 있는 통합 마스터 저장소입니다.

## 📂 디렉토리 구조 (Directory Structure)

### 1. `sodam-pwa/` (당목담글 PWA 웹앱)
- **목적**: 사용자가 자신의 목소리로 릴레이 낭독을 기부할 수 있는 모바일 최적화 웹 애플리케이션입니다.
- **기술 스택**: React, Vite, Firebase (Firestore & Hosting)
- **주요 기능**: 
  - 브라우저 내장 마이크를 활용한 음성 녹음 및 Base64 인코딩 저장
  - Firebase DB 기반의 캠페인별 분리 저장 (`campaigns/{캠페인명}/participants`)
  - 랜덤 코르크 보드 형태의 '명예의 전당' UI (오디오 재생 지원)
- **배포 주소 (Live URL)**: [https://dmdg-ut.web.app/sodam-web](https://dmdg-ut.web.app/sodam-web)
- **실행 방법**: `cd sodam-pwa` -> `npm install` -> `npm run dev`

### 2. `YOUTUBE/` (유튜브 콘텐츠 제작 및 자동화 파이프라인)
- **목적**: 플랫폼 홍보용 비디오 콘텐츠를 렌더링하고 합성하기 위한 자동화 환경입니다. 모든 파이썬 스크립트는 파일 탐색기 정리를 위해 `YOUTUBE/scripts/` 폴더 하위에 모아서 관리됩니다.
- **주요 폴더 및 파일 구조**:
  - `ffmpeg.exe`, `ffprobe.exe`, `ffplay.exe`: 영상 및 음성 합성에 사용되는 로컬 FFmpeg 바이너리 엔진.
  - `scripts/`: 자동화 및 합성을 처리하는 파이썬 실행 스크립트 폴더.
    - `check_and_copy.py`: 수묵화 이미지 복사 및 비디오 렌더링 전체 제어 스크립트.
    - `render_shorts_subway.py`: 이미지 컷 전환(슬라이드 쇼) 및 안전 자막 마진이 적용된 지하철 쇼츠 렌더링 코어.
    - (그 외 TTS 생성, 오디오 믹싱, 명성황후 롱폼 빌드 등 모든 `.py` 스크립트 격리 보관)
  - `Projects/`: 개별 비디오 콘텐츠 프로젝트 영역.
    - `Empress_Longform/`: 명성황후 롱폼 프로젝트 영역.
    - `Subway_Shorts/`: 지하철 잔혹사 쇼츠 프로젝트 영역.
      - `assets_audio/`: 다국어(KOR, ENG, JPN) 나레이션 음성 폴더.
      - `assets_image/`: 씬별로 매칭되는 100% 수묵화(Sumukhwa) 일러스트 폴더 (구형 실사 및 외국인 사진 삭제 완).
      - `exports/`: 합성이 완료된 다국어 최종 쇼츠 비디오 파일 보관 폴더.

### 3. `AI_Knowledge_Base/` (사내 AI / RAG 데이터베이스)
- **목적**: 당목담글(DMDG)만의 페르소나와 톤앤매너를 지닌 커스텀 AI 모델(RAG 시스템)을 학습시키기 위한 전용 아카이브입니다.
- **주요 구성**:
  - `meetings/` : 회의록, 주요 의사결정 로그 백업 (구 `회의록/` 폴더 역할 대체)
  - `guidelines/` : 유튜브 썸네일 규칙, 어그로/도파민 유도 전략 가이드라인
  - `instructions/` : 과거 수행했던 작업 지시서 모음

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
