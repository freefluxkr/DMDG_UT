---
id: meeting-local-model-strategy
title: "AI 모델 전략 및 로드맵 논의"
date: 2026-05-25
participants: ["사장님", "레오(AI)"]
tags:
  - #회의록
  - #AI모델
  - #전략
  - #KVJ_V2
---

# 🧠 AI 모델 운용 전략 및 글로벌 로드맵 회의록

## 1. 글로벌 서비스 로드맵 리뷰
- `global_service_roadmap.md` 문서를 검토하며 K-Virtual Journey의 글로벌 확장을 위한 전체 방향성 얼라인 완료.

## 2. AI 모델 사용 현황 및 로컬 모델 전략 논의
- **이슈**: "현재 어떤 모델을 사용하고 있는지?", "로컬 모델을 당장 사용하지 않는 이유는 무엇인지?"에 대한 사장님의 질의.
- **현황 보고**: 
  - 현재 레오(AI) 본체는 클라우드 기반의 강력한 `Gemini 3.1 Pro` 모델을 바탕으로 복잡한 기획 및 코딩을 수행 중.
  - `antigravity.config.json` 내에는 `gemma2:2b` 로컬 모델 설정이 이미 준비되어 있음.
- **결론**: 
  - 방대한 리소스가 필요한 대규모 구조 설계는 클라우드 API를 사용하고, 빠른 응답과 프라이버시가 중요한 반복 태스크(예: NPC 대화 생성)에는 점진적으로 로컬 모델(`gemma2:2b`)을 혼합하여 사용하는 하이브리드 전략을 취하기로 함.
  - 향후 `@local` 명령어 호출 시 로컬 API를 직접 핑(Ping)할 수 있는 체계 마련 예정. (이후 `query_local.py` 작성으로 이어짐)

## 🔗 연관 지식
- [[global_service_roadmap]]
- [[local_model_strategy]]
- [[antigravity.config.json]]
