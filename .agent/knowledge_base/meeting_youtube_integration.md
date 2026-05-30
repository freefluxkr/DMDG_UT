---
id: meeting-youtube-integration
title: "YouTube API 연동 및 지식 베이스 구축"
date: 2026-05-20
participants: ["사장님", "레오(AI)"]
tags:
  - #회의록
  - #개발
  - #YouTube_API
  - #지식그래프
  - #SecondBrain
---

# 🧠 유튜브 콘텐츠 지식화 프로젝트 회의록

## 1. Gemini Omni API 연동 논의
- 사장님의 "Gemini omni API 연결 가능성" 질의에 대해, Gemini 1.5 Pro/Flash의 멀티모달 처리 능력을 활용한 파이썬 연동 방안 보고 완료.

## 2. 유튜브 채널 지식화 자동화 구축
- **목표**: 사장님의 유튜브 채널 모든 콘텐츠를 가져와 Obsidian 스타일의 지식 노드로 구조화.
- **포맷 지정**:
  - `📌 Brief Summary`: 핵심 요약
  - `📖 Core Content`: 상세 내용
  - `🔗 Knowledge Connections`: 연관 개념 및 프로젝트 (Wikilink)
- **개발 내역**:
  - `youtube.readonly` 권한을 이용한 `youtube_knowledge_builder.py` 스크립트 작성 완료.
  - API 인증을 거쳐 영상 메타데이터를 파싱하고 `.agent/knowledge_base/youtube/` 폴더에 마크다운 파일로 자동 변환하여 21개의 지식 파일 생성 완료.

## 3. 유튜브 알고리즘 기획 
- 구축된 21개의 유튜브 지식 파일을 모두 분석하여, "다음 유튜브 콘텐츠로 알고리즘이 터질 만한" 후속 콘텐츠 기획 진행.

## 🔗 연관 지식
- [[youtube_knowledge_builder]]
- [[Gemini_API]]
