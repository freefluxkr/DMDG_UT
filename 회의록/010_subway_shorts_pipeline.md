# 🚇 숏츠 영상 제작 파이프라인 기획안: 서울 지하철 잔혹사

> **프로젝트명**: 서울 지하철 잔혹사 (Seoul Subway Chronicles)
> **채널**: @anti-korea
> **포맷**: YouTube Shorts (세로형, 약 60초)
> **언어**: KOR / ENG / JPN (3개 버전 개별 출력)
> **목표**: 알고리즘 최적화 + 댓글 참여 유도 + 구독자 전환

---

## 📌 전체 파이프라인 개요

```
[PHASE 1] 대본 & 기획
      ↓
[PHASE 2] 에셋 생성 (이미지 + TTS 오디오)
      ↓
[PHASE 3] 영상 편집 & 믹싱
      ↓
[PHASE 4] 자막 & 다국어 처리
      ↓
[PHASE 5] 썸네일 제작
      ↓
[PHASE 6] 업로드 & 메타데이터 최적화
      ↓
[PHASE 7] 퍼포먼스 모니터링
```

---

## [PHASE 1] 대본 & 기획 ✍️

### 담당자: 무라카미 하루키 (스토리 디렉터)

| 항목 | 내용 | 산출물 |
|---|---|---|
| 씬 구성 | HOOK(5초) + SCENE×3(각 15초) + OUTRO(10초) | `008_shorts_script_subway_manners.md` ✅ |
| 나레이션 대본 | KOR/ENG/JPN 3언어 작성 | 위 파일 내 포함 ✅ |
| 어그로 포인트 | "미안하다는 말은 사치품", "에어팟 귀족" 등 자극 워딩 | 위 파일 내 포함 ✅ |
| SFX/BGM 지시사항 | 씬별 효과음 & 분위기 정의 | 위 파일 내 포함 ✅ |

> **✅ PHASE 1 완료** — `008_shorts_script_subway_manners.md` 참조

---

## [PHASE 2] 에셋 생성 🎨🎙️

### 2-1. 이미지 에셋 (AI 이미지 생성)

#### 필요 컷 목록

| 씬 | 컷 번호 | 묘사 | 스타일 |
|---|---|---|---|
| HOOK | `IMG_00_hook` | 끝없이 내려가는 지하철 에스컬레이터 하강 1인칭 뷰 | 다크/모노톤, 형광등 조명 |
| SCENE 1 | `IMG_01a_bump` | 노량진역 환승통로 어깨빵 순간 (핸드헬드 흔들림 느낌) | 붉은 비상구 조명 그림자 강조 |
| SCENE 1 | `IMG_01b_tokyo` | 도쿄 신주쿠 인파 오버랩 컷 | 차갑고 흐릿한 이중노출 |
| SCENE 2 | `IMG_02_salmon` | 왕십리역 계단 새치기 로우앵글 | 줄 선 사람=어둡게, 새치기=스포트라이트 |
| SCENE 3 | `IMG_03_noble` | GTX 내부 경로석, 에어팟+스마트폰 블루라이트 얼굴 줌인 | 사이버펑크, 슬로우 줌 |
| OUTRO | `IMG_04_door` | 닫히는 스크린도어 + 유리에 반사된 지친 얼굴들 | 암전 직전, 양쪽에서 닫히는 구도 |

#### 이미지 생성 도구
- **도구**: Midjourney / DALL-E 3 / Stable Diffusion
- **비율**: `9:16` (1080×1920px) — Shorts 전용
- **저장 경로**: `YOUTUBE/Projects/Subway_Shorts/assets_image/`

---

### 2-2. TTS 오디오 에셋 (나레이션 생성)

#### 생성 스크립트
```bash
# YOUTUBE 디렉토리에서 실행
python generate_tts_subway.py
```

> 📁 스크립트 경로: [`generate_tts_subway.py`](file:///c:/Users/user/Documents/DMDG_UT/YOUTUBE/generate_tts_subway.py)

#### 출력 파일 구조
```
YOUTUBE/Projects/Subway_Shorts/assets_audio/
├── kor/
│   ├── 00_hook_kor.mp3
│   ├── 01_scene1_kor.mp3
│   ├── 02_scene2_kor.mp3
│   ├── 03_scene3_kor.mp3
│   └── 04_outro_kor.mp3
├── eng/
│   └── (동일 구조)
└── jpn/
    └── (동일 구조)
```

#### TTS 음성 설정 (강하루 캐릭터)
| 파라미터 | 설정값 |
|---|---|
| 성별 | 여성 (차분하고 냉소적인 톤) |
| 속도(Speed) | 0.95 (살짝 느림, 여운 강조) |
| 피치(Pitch) | -1 (낮고 묵직하게) |
| 엔진 | `sgamma4:latest` (로컬 모델) |

---

## [PHASE 3] 영상 편집 & 믹싱 🎬

### 편집 세팅
- **해상도**: 1080 × 1920 (9:16 세로형)
- **프레임레이트**: 30fps
- **편집 툴**: CapCut / DaVinci Resolve (권장)

### 3-1. 타임라인 뼈대 구성 순서

```
1. KOR 오디오 트랙을 타임라인에 먼저 배치 (뼈대)
2. 각 씬 이미지를 오디오 길이에 맞춰 배치
3. BGM 트랙 추가 (볼륨 -15dB, 나레이션 하위)
4. SFX 트랙 추가 (씬 전환점에 맞춤 배치)
```

### 3-2. 씬별 무빙 효과 (Ken Burns Effect)

| 씬 | 효과 | 파라미터 |
|---|---|---|
| HOOK | 빠른 하강 줌인 (Vertigo) | Scale 100% → 130%, Duration 5초 |
| SCENE 1 | 핸드헬드 쉐이킹 | X축 ±5px 랜덤 진동, 충돌 순간 강조 |
| SCENE 2 | 로우앵글 패닝 (하→상) | Y축 +30px → 0px, Duration 15초 |
| SCENE 3 | 슬로우 줌인 | Scale 100% → 115%, Duration 15초 (서서히) |
| OUTRO | 양쪽 Wipe to Black | 스크린도어 닫히는 방향으로 |

### 3-3. BGM 설계

| 구간 | BGM | 톤 |
|---|---|---|
| HOOK (0~5s) | 한스 짐머 스타일 테크노 첼로 비트 시작 | 차갑고 빠른 상승 |
| SCENE 1~3 (5~50s) | 베이스 드롭 + 심박 드럼 | 위압적, 규칙적 |
| OUTRO (50~60s) | 갑작스런 컷 → 완전한 정적 | 감정 여운 극대화 |

### 3-4. SFX 타이밍

| 타임코드 | 효과음 | 설명 |
|---|---|---|
| 00:00 | `지하철 진동음 "우우웅-"` | HOOK 시작과 동시 |
| 00:07 | `어깨 충돌음 "퍽!"` | SCENE 1 핵심 순간 |
| 00:20 | `구두 발소리 "다다다닥"` | SCENE 2 새치기 시작 |
| 00:35 | `이명음 "삐~" + BGM 먹먹 뮤트` | SCENE 3 에어팟 효과 |
| 00:50 | `스크린도어 경고음 "삐-삐-삐-"` | OUTRO 시작 |
| 00:57 | `문 닫히는 파열음 → 정적` | 블랙아웃 직전 |

---

## [PHASE 4] 자막 & 다국어 처리 🌏

### 자막 스타일 가이드
- **폰트**: 나눔명조 Bold / 마포 꽃섬 (한국어)
- **위치**: 화면 하단 1/4, 시네마틱 블랙바 위
- **크기**: 48px (모바일 기준 가독성 확보)
- **색상**: 흰색 텍스트 + 블랙 아웃라인 2px

### 3개 버전 출력 전략

| 버전 | 오디오 | 자막 | 파일명 |
|---|---|---|---|
| KOR | `kor/*.mp3` | 한국어 자막 | `subway_shorts_KOR_final.mp4` |
| ENG | `eng/*.mp3` | English subtitle | `subway_shorts_ENG_final.mp4` |
| JPN | `jpn/*.mp3` | 日本語字幕 | `subway_shorts_JPN_final.mp4` |

> **💡 팁**: KOR 버전을 마스터로 편집 완료 후, 오디오 트랙만 교체 + 자막만 교체하여 ENG/JPN 버전 파생

---

## [PHASE 5] 썸네일 제작 🖼️

> 참조: [`004_thumbnail_planning.md`](file:///c:/Users/user/Documents/DMDG_UT/회의록/004_thumbnail_planning.md)

### anti-korea 채널용 썸네일 가이드 (쇼츠 티저)

| 항목 | 설정 |
|---|---|
| **사이즈** | 1080 × 1920 (Shorts 커버) |
| **핵심 이미지** | 어두운 지하철 + 강렬한 인물 표정 (클로즈업) |
| **텍스트 1** | `서울 지하철 잔혹사` (굵은 고딕, 중앙 하단) |
| **텍스트 2** | `당신의 출근길은 안녕하십니까?` (명조, 소형) |
| **색감** | 다크 모노크롬 + 붉은 포인트 (비상구 조명 컬러) |
| **로고** | 당목담글 로고 상단 우측 (반투명 30%) |

---

## [PHASE 6] 업로드 & 메타데이터 최적화 📤

### 유튜브 업로드 체크리스트

- [ ] KOR 버전 업로드 (`subway_shorts_KOR_final.mp4`)
- [ ] 제목: `서울 지하철 잔혹사 | 출근길의 민낯 🚇💀 #지옥철 #Shorts`
- [ ] 설명란: 3언어 채널 링크 + 관련 영상 링크 삽입
- [ ] 썸네일 업로드
- [ ] 해시태그 설정 (15개 이하 권장)

```
#지옥철 #어깨빵 #부츠카리오토코 #지하철매너 #새치기 
#GTX #빌런 #분노유발 #공감쇼츠 #한국지하철 
#antikorea #Shorts #서울 #출근길 #지하철잔혹사
```

- [ ] ENG/JPN 버전 별도 업로드 또는 다중 자막 추가
- [ ] 첫 24시간 댓글 모니터링 → 고정 댓글 선정 (공감 유도)

---

## [PHASE 7] 퍼포먼스 모니터링 📊

### KPI (핵심 지표)

| 지표 | 목표 (72시간 내) |
|---|---|
| 조회수 | 10,000+ |
| 시청 완료율 (60초) | 40% 이상 |
| 좋아요 / 싫어요 비율 | 논쟁 유도 (댓글 수 > 좋아요 수) |
| 댓글 수 | 100+ (경험담, 반박, 공감) |
| 공유 수 | 50+ |

### 알고리즘 가속 전략
- 업로드 후 **30분 이내** 팀 내 조회 + 좋아요 + 댓글 선점
- 고정 댓글: `"여러분이 겪은 최악의 지옥철 매너는? 댓글로 알려주세요 👇"`
- 인스타그램 / X(트위터) 티저 클립 동시 배포

---

## 📁 최종 디렉토리 구조

```
YOUTUBE/Projects/Subway_Shorts/
├── assets_image/          ← AI 생성 이미지 컷 (Phase 2)
│   ├── IMG_00_hook.png
│   ├── IMG_01a_bump.png
│   ├── IMG_01b_tokyo.png
│   ├── IMG_02_salmon.png
│   ├── IMG_03_noble.png
│   └── IMG_04_door.png
├── assets_audio/          ← TTS 나레이션 오디오 (Phase 2)
│   ├── kor/
│   ├── eng/
│   └── jpn/
├── assets_bgm/            ← BGM & SFX 파일
├── edit_project/          ← CapCut/DaVinci 프로젝트 파일
├── thumbnail/             ← 썸네일 이미지
│   └── thumbnail_subway_shorts.png
└── result/                ← 최종 렌더링 결과물
    ├── subway_shorts_KOR_final.mp4
    ├── subway_shorts_ENG_final.mp4
    └── subway_shorts_JPN_final.mp4
```

---

## ✅ 현재 진행 상태

| Phase | 상태 | 비고 |
|---|---|---|
| PHASE 1: 대본 & 기획 | ✅ 완료 | `008_shorts_script_subway_manners.md` |
| PHASE 2: 이미지 에셋 | ⏳ 대기 | AI 이미지 생성 필요 |
| PHASE 2: TTS 오디오 | ⏳ 대기 | `generate_tts_subway.py` 실행 필요 |
| PHASE 3: 영상 편집 | ⏳ 대기 | Phase 2 완료 후 |
| PHASE 4: 자막 처리 | ⏳ 대기 | Phase 3 완료 후 |
| PHASE 5: 썸네일 | ⏳ 대기 | AI 이미지 생성 병행 가능 |
| PHASE 6: 업로드 | ⏳ 대기 | 모든 Phase 완료 후 |
| PHASE 7: 모니터링 | ⏳ 대기 | 업로드 후 즉시 시작 |

---

*작성일: 2026-06-01 | 작성: 무라카미 하루키 (스토리 디렉터) + AI 어시스턴트*
