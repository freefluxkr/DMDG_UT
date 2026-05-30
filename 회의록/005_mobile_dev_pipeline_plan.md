# 모바일 프론트엔드 개발 파이프라인 및 반응형 테스트 기획

본 기획안은 당목담글 웹앱의 실제 프론트엔드 개발 파이프라인을 가동하기 전, 한국 시장 점유율 기반의 스마트폰 뷰포트(Viewport) 조사 결과와 이에 따른 크로스 브라우징/디바이스 테스트 전략을 정의합니다.

## 1. 한국 시장 스마트폰 뷰포트 조사 (2024-2025 기준)

물리적 해상도(Resolution)가 아닌, CSS 렌더링 기준인 **논리적 뷰포트(Viewport)**를 기준으로 분석했습니다. 한국은 삼성 갤럭시(Android)와 아이폰(iOS) 점유율이 압도적입니다.

- **안드로이드 (Samsung Galaxy 주력):**
  - 가장 일반적인 뷰포트: `360px × 780px` ~ `412px × 892px` (S시리즈 및 A시리즈)
- **아이폰 (iOS 주력):**
  - 일반 ~ Pro 라인: `390px × 844px` ~ `393px × 852px` (iPhone 13, 14, 15)
  - Pro Max 라인: `430px × 932px`

### 전략적 결론 (Breakpoints)
모든 UI 요소는 가장 작은 뷰포트인 **360px**에서 텍스트 잘림 현상이 없는지 1차로 보장해야 하며, 최대 **430px**까지 유동적(Fluid)으로 늘어나도록 `rem` 및 `%` 단위를 혼용하여 개발해야 합니다. (PC 환경 접근 시에는 기존처럼 Max-width 480px의 컨테이너를 유지)

---

## 2. 개발 및 테스트 파이프라인 (Pipeline)

### [Phase 1] 개발 환경 세팅 (Development)
- **Vite + React (혹은 Vanilla JS) 프로젝트 스캐폴딩:** 빠르고 가벼운 렌더링을 위해 최신 번들러 환경 구축.
- **디자인 토큰 이관:** Stitch에서 정의한 `Forest & Mustard` 컬러 HEX 코드, 폰트(Noto Sans KR), Spacing 시스템을 CSS 변수(Variables)로 추출하여 전역(Global) 설정.

### [Phase 2] 반응형 컴포넌트 이식 (Integration)
- 메인, 마중물(기부), 서재(상세) 화면의 정적 HTML을 재사용 가능한 컴포넌트로 분리.
- `min-width: 360px` ~ `max-width: 480px` 사이의 Fluid Typography 적용 (화면이 커지면 글자도 미세하게 커지는 반응형).

### [Phase 3] 디바이스 단위 테스트 (Testing & QA)

- **Safe Area 대응 방안:** CSS `padding-bottom: env(safe-area-inset-bottom);`를 반드시 적용하여 아이폰의 하단 홈 인디케이터와 탭 버튼이 겹치지 않게 처리.
- Chrome DevTools의 Device Mode를 활용하여 `Galaxy S22 (360px)` 및 `iPhone 14 Pro (393px)` 기준 시뮬레이션 테스트 우선 진행.
