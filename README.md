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
- **실행 방법**: `cd sodam-pwa` -> `npm install` -> `npm run dev`

### 2. `YOUTUBE/` (웹툰 30컷 렌더링 파이프라인)
- **목적**: 당목담글 플랫폼 홍보를 위한 롱폼/쇼츠 유튜브 영상 제작용 파이프라인.
- **주요 구성**:
  - `characters/`: '더피' 등 프로젝트 공식 에셋 보관소.
  - `result/`: AI가 렌더링한 배경 이미지 및 파이썬을 통해 공식 에셋이 합성된 최종 컷 보관.
  - `render_*.py`: 이미지 생성, 자막 합성, TTS 음성 생성, 최종 영상 렌더링을 자동화하는 Python 스크립트 모음.

### 3. `회의록/` (기획 문서)
- 기획 의도, 스토리보드, AI 에이전트(Master, Demis, Peggy, Mustafa) 페르소나 및 협업 룰 문서화.

## 🤖 AI Agents Team (마스터 & 어벤져스)
이 프로젝트는 인간 마스터(사장님)의 지휘 아래, 다음의 AI 에이전트들이 분업하여 구축되었습니다.
*   **Master**: 총괄 기획 및 최종 승인자 (사장님)
*   **Demis (CEO)**: 프로젝트 전략 수립, PWA 비즈니스 로직 및 전체 흐름 통제
*   **Peggy (Art Director)**: UI/UX 디자인, 수묵화풍 웹툰 프롬프트 엔지니어링 및 렌더링
*   **Mustafa (Infra)**: Firebase DB 구조화, Python 영상/오디오 파이프라인 아키텍처 설계 및 자동화 스크립트 작성

---
> **참고**: PWA 내부의 `node_modules`와 Python 임시 캐시 파일들은 `.gitignore`를 통해 업로드에서 제외되었습니다. 코드를 클론(Clone) 받은 후 반드시 `npm install` 등의 초기 세팅을 진행해주세요.

## 🔄 프로젝트 복구 및 초기 세팅 가이드 (Antigravity 재설치 시)

만약 PC를 포맷하거나 Antigravity(AI 에이전트)를 새로 설치하여 처음부터 다시 시작해야 할 경우, 다음 순서대로 진행해 주세요.

### 1. 소스코드 내려받기 (Clone)
터미널(또는 Antigravity 파워쉘)을 열고 원하는 폴더(예: `D:\`)에서 아래 명령어를 실행합니다.
```bash
git clone https://github.com/freefluxkr/DMDG_UT.git
```
명령어가 완료되면 `D:\DMDG_UT` 폴더가 생성되고 모든 코드가 다운로드됩니다.

### 2. Antigravity에게 컨텍스트 부여하기
새로 설치된 Antigravity에게 프로젝트를 설명하려면, 채팅창에 다음과 같이 입력하세요:
> "D:\DMDG_UT 폴더에 있는 프로젝트야. README.md 파일과 회의록 폴더를 먼저 읽고 현재 상황과 내(Master) 역할, 그리고 너희 팀(Demis, Peggy, Mustafa)의 역할을 파악해 줘."

### 3. PWA 웹앱 실행 준비
의존성(라이브러리) 모듈을 다시 설치해야 정상적으로 웹앱을 실행할 수 있습니다.
```bash
cd D:\DMDG_UT\sodam-pwa
npm install
npm run dev
```

### 4. 백업 스크립트 실행 (선택)
작업을 마친 뒤 다시 GitHub에 백업하고 싶다면 `D:\DMDG_UT` 최상단 폴더에서 다음 명령어들을 순서대로 실행하세요.
```bash
git add .
git commit -m "작업 내용 요약"
git push
```
