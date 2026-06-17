import asyncio
import edge_tts
import os
import re
import json
import sys
from pydub import AudioSegment

# 1. FFmpeg & FFprobe 경로를 시스템 PATH 환경변수에 동적 주입 (pydub 에러 방지)
FFMPEG_DIR = r"C:\Users\tuesv\Documents\DMDG_UT\YOUTUBE"
if os.path.exists(FFMPEG_DIR):
    os.environ["PATH"] += os.pathsep + FFMPEG_DIR
    print(f"Added FFmpeg path to environment: {FFMPEG_DIR}", flush=True)

# 9인 캐릭터별 음성 스펙 설정 (로봇 소리 배제를 위해 순정 뉴럴 보이스로 통일)
CHARACTER_VOICES = {
    "소통 매니저": {"voice": "ko-KR-SunHiNeural", "rate": "+8%", "pitch": "+2Hz"},
    "UI/UX 디자이너": {"voice": "ko-KR-SunHiNeural", "rate": "+2%", "pitch": "+0Hz"},
    "대표": {"voice": "ko-KR-InJoonNeural", "rate": "-2%", "pitch": "-4Hz"},
    "풀스택 개발자": {"voice": "ko-KR-HyunsuMultilingualNeural", "rate": "+15%", "pitch": "+4Hz"},
    "시니어 아키텍트": {"voice": "ko-KR-InJoonNeural", "rate": "-6%", "pitch": "-6Hz"},
    "데이터 분석가": {"voice": "ko-KR-HyunsuMultilingualNeural", "rate": "+4%", "pitch": "-1Hz"},
    "스토리 작가": {"voice": "ko-KR-SunHiNeural", "rate": "-5%", "pitch": "-3Hz"},
    "음향 감독": {"voice": "ko-KR-InJoonNeural", "rate": "+0%", "pitch": "+2Hz"},
    "버그 탐정": {"voice": "ko-KR-HyunsuMultilingualNeural", "rate": "+8%", "pitch": "+1Hz"},
}

# 텍스트에 들어있는 마크다운이나 코드 문장 부호들을 TTS가 자연스럽게 읽도록 정제하는 함수
def clean_tts_text(text):
    # 소괄호 (...) 안의 연출 주석 내용 완전 제거 (예: 효과음 설명 등)
    text = re.sub(r'\(.*?\)', '', text)
    text = text.replace('**', '')
    text = text.replace('*', '')
    text = text.replace('`', '')
    text = text.replace('...', '... ')
    text = text.replace('SQLite WAL', '에스큐엘라이트 왈')
    text = text.replace('SQLite', '에스큐엘라이트')
    text = text.replace('WAL', '왈')
    text = text.replace('Redis', '레디스')
    text = text.replace('FastAPI', '패스트 에이피아이')
    text = text.replace('Watchdog', '왓치독')
    text = text.replace('Queue', '큐')
    text = text.replace('try-except', '트라이 엑셉트')
    text = text.replace('Fault Tolerance', '결함 허용')
    text = text.replace('WebGL', '웹쥐엘')
    text = text.replace('Lottie', '로티')
    text = text.replace('SVG', '에스브이지')
    text = text.replace('GPU', '지피유')
    text = text.replace('stdout', '스탠다드 아웃풋')
    text = text.replace('sys.stdout.flush()', '시스 닷 스탠다드 아웃풋 플러시')
    text = text.replace('CP949', '씨피 구사구')
    text = text.replace('UTF-8', '유티에프 에잇')
    text = text.replace('UnicodeDecodeError', '유니코드 디코드 에러')
    text = text.replace('UX', '유엑스')
    text = text.replace('UI', '유아이')
    text = text.replace('BM', '비엠')
    text = text.replace('CEO', '씨이오')
    return text.strip()

# 대사 파일 파싱 함수
def parse_script(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 씬(Scene) 단위로 스크립트를 분할
    scenes_raw = re.split(r"### 🎥 \[Scene \d+\]", content)
    # 첫 조각은 헤더 정보이므로 제외
    scenes_raw = scenes_raw[1:]

    parsed_scenes = []
    
    for idx, scene_content in enumerate(scenes_raw):
        scene_num = idx + 1
        lines = scene_content.split("\n")
        scene_lines = []
        
        current_character = None
        current_speech_lines = []

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            
            # 1. 발언 캐릭터 탐지: 줄이 '*'로 시작하고 끝이 ':'인 발언 라인인지 확인
            is_char_line = line_str.startswith("*") and line_str.endswith(":") and "[" in line_str and "]" in line_str
            if is_char_line:
                # 이전 캐릭터 대사가 있으면 누적 저장
                if current_character and current_speech_lines:
                    full_text = " ".join(current_speech_lines)
                    scene_lines.append((current_character, full_text))
                    current_speech_lines = []
                
                # 대괄호 안의 역할명만 추출
                char_match = re.search(r"\[([^\]]+)\]", line_str)
                if char_match:
                    current_character = char_match.group(1).strip()
                continue
            
            elif line_str.startswith("*"):
                # 캐릭터 발언 라인이 아닌데 별표로 시작하면 비주얼/효과음 단락의 시작이므로 수집 중단
                if current_character and current_speech_lines:
                    full_text = " ".join(current_speech_lines)
                    scene_lines.append((current_character, full_text))
                    current_speech_lines = []
                current_character = None
                continue
            
            # 2. 대사 내용 분석: 줄이 '-'로 시작하면 대사 라인임
            if current_character and line_str.startswith("-"):
                # 연출 주석이나 비주얼 필드는 건너뜀 (예: - **좌측 영역**: 등)
                if "**" in line_str and ":" in line_str:
                    continue
                
                # 대사 텍스트 양 끝의 불필요한 기호(- , " ) 제거
                speech_text = line_str.lstrip("- ").strip()
                if speech_text.startswith('"') and speech_text.endswith('"'):
                    speech_text = speech_text[1:-1]
                
                if speech_text:
                    current_speech_lines.append(speech_text)
        
        # 마지막 대사 누적 저장
        if current_character and current_speech_lines:
            full_text = " ".join(current_speech_lines)
            scene_lines.append((current_character, full_text))
            
        parsed_scenes.append((scene_num, scene_lines))
        
    return parsed_scenes

async def generate_scene_audio(scene_num, scene_lines, output_dir, timings_data):
    temp_files = []
    scene_audio = AudioSegment.empty()
    
    print(f"\n--- Scene {scene_num} Audio Generation Started (Total {len(scene_lines)} lines) ---", flush=True)
    if len(scene_lines) == 0:
        print(f"  (Warning: No lines parsed in Scene {scene_num})", flush=True)
        return
        
    scene_timings = []
    
    for line_idx, (character, text) in enumerate(scene_lines):
        clean_text = clean_tts_text(text)
        if not clean_text:
            continue
            
        voice_spec = CHARACTER_VOICES.get(character, {"voice": "ko-KR-InJoonNeural", "rate": "+0%", "pitch": "+0Hz"})
        
        temp_filename = f"temp_s{scene_num}_{line_idx:03d}.mp3"
        temp_filepath = os.path.join(output_dir, temp_filename)
        
        # edge-tts로 음성 바이너리 생성
        communicate = edge_tts.Communicate(clean_text, voice_spec["voice"], rate=voice_spec["rate"], pitch=voice_spec["pitch"])
        await communicate.save(temp_filepath)
        temp_files.append(temp_filepath)
        
        # pydub으로 재생 시간 확인 및 병합
        line_audio = AudioSegment.from_file(temp_filepath, format="mp3")
        duration_ms = len(line_audio)
        
        # 씬 내 대사 병합 및 0.6초(600ms) 텀 제공
        scene_audio += line_audio + AudioSegment.silent(duration=600)
        
        # 타이밍 데이터 누적
        scene_timings.append({
            "character": character,
            "text": text,
            "duration_ms": duration_ms,
            "silence_ms": 600
        })
        
        print(f"  [{character}] ({duration_ms}ms): {clean_text[:40]}...", flush=True)

    # 씬 최종 mp3 파일 저장
    scene_output_path = os.path.join(output_dir, f"scene{scene_num}_mixed.mp3")
    scene_audio.export(scene_output_path, format="mp3")
    print(f"-> Scene {scene_num} Mixed Audio Saved: {scene_output_path}", flush=True)
    
    # 임시 파일 삭제
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except Exception:
            pass
            
    timings_data[f"scene{scene_num}"] = scene_timings

async def main():
    root_dir = r"c:\Users\tuesv\Documents\DMDG_UT"
    script_path = os.path.join(root_dir, "회의록", "036_youtube_friendly_office_discussion.md")
    audio_dir = os.path.join(root_dir, "media", "audio")
    
    os.makedirs(audio_dir, exist_ok=True)
    
    parsed_scenes = parse_script(script_path)
    
    timings_data = {}
    
    for scene_num, scene_lines in parsed_scenes:
        await generate_scene_audio(scene_num, scene_lines, audio_dir, timings_data)
        
    # 타이밍 데이터를 JSON으로 출력 저장
    timings_json_path = os.path.join(audio_dir, "scene_timings.json")
    with open(timings_json_path, "w", encoding="utf-8") as jf:
        json.dump(timings_data, jf, ensure_ascii=False, indent=2)
    print(f"\n[SUCCESS] All longform scene audios and timings.json saved successfully at: {timings_json_path}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
