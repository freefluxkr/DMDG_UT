import os
import subprocess

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
PROJECT_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Subway_Smell")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "assets_썸네일")
FFMPEG_EXE = os.path.join(YOUTUBE_DIR, "ffmpeg.exe")

# 입력 이미지 설정 (AI 생성 이미지)
INPUT_IMAGE = r"C:\Users\tuesv\.gemini\antigravity-ide\brain\a41f3005-55f0-4aef-8937-e54a21adf2e5\subway_smell_thumbnail_base_1781058760240.png"

# 출력 폴더 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 폰트 경로 (Windows 기본 맑은 고딕 Bold)
FONT_PATH = "C\\:/Windows/Fonts/malgunbd.ttf"

# 언어별 텍스트 설정
thumbnail_configs = {
    "KOR": {
        "output": os.path.join(OUTPUT_DIR, "thumbnail_KOR.png"),
        "texts": [
            {"text": "코 마비 경보!", "size": 85, "y": 350, "color": "yellow"},
            {"text": "지하철 냄새 탈출법", "size": 85, "y": 480, "color": "yellow"}
        ]
    },
    "ENG": {
        "output": os.path.join(OUTPUT_DIR, "thumbnail_ENG.png"),
        "texts": [
            {"text": "ODOR ALERT!", "size": 85, "y": 350, "color": "yellow"},
            {"text": "Subway Smell Guide", "size": 80, "y": 480, "color": "yellow"}
        ]
    },
    "JPN": {
        "output": os.path.join(OUTPUT_DIR, "thumbnail_JPN.png"),
        "texts": [
            {"text": "鼻が曲がる！", "size": 85, "y": 350, "color": "yellow"},
            {"text": "地下鉄の臭い脱출법", "size": 80, "y": 480, "color": "yellow"}  # 일본어 폰트에 대응하도록 한자 및 일어로 구성
        ]
    }
}

# JPN 텍스트 중 '탈출법'은 일본어 '脱出法'로 기재되어야 합니다. (오타 수정 반영)
thumbnail_configs["JPN"]["texts"][1]["text"] = "地下鉄の臭い脱出法"

def build_drawtext_filter(texts):
    filters = []
    for t in texts:
        # 특수문자 및 콜론 에스케이프 처리
        text_escaped = t["text"].replace("'", "'\\\\\\''").replace(":", "\\:")
        filt = (
            f"drawtext=fontfile='{FONT_PATH}':text='{text_escaped}':"
            f"x=(w-text_w)/2:y={t['y']}:fontsize={t['size']}:"
            f"fontcolor={t['color']}:borderw=6:bordercolor=black"
        )
        filters.append(filt)
    return ",".join(filters)

def main():
    print("==============================================")
    # 썸네일 생성 시작
    print("3개국어 유튜브 쇼츠 썸네일 이미지 합성 시작...")
    print("==============================================")
    
    if not os.path.exists(INPUT_IMAGE):
        print(f"[에러] 입력 베이스 이미지가 존재하지 않습니다: {INPUT_IMAGE}")
        return
        
    for lang, config in thumbnail_configs.items():
        print(f"\n[{lang} 버전 썸네일 합성 중...]")
        filter_str = build_drawtext_filter(config["texts"])
        
        cmd = [
            FFMPEG_EXE, "-y",
            "-i", INPUT_IMAGE,
            "-vf", filter_str,
            config["output"]
        ]
        
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(config["output"]):
                print(f"[성공] 썸네일 생성 완료: {config['output']}")
            else:
                print(f"[실패] 합성 중 오류 발생:\n{res.stderr}")
        except Exception as e:
            print(f"[실패] 실행 실패: {e}")

if __name__ == "__main__":
    main()
