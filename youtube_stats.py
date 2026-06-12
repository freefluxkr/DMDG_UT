import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# .env 파일 로드
load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')

# 실제 유튜브 채널 ID
CHANNELS = {
    '@anti-korea': 'UCW8OsY6gfQn4z0sLRS-ErOw', 
    '@dmdg-free': 'UC6tcqStNeSzoe7Kv0iFECUA'
}

def generate_report():
    if not API_KEY or API_KEY.startswith('AIzaSy_여기'):
        return "⚠️ **오류**: `.env` 파일에 유튜브 API 키가 입력되지 않았습니다!\n(루트 폴더의 `.env` 파일을 열어서 `YOUTUBE_API_KEY` 값에 진짜 키를 입력해주세요!)"
    
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        report = "🔥 **유튜브 실시간 채널 통계 (API 연동)**\n\n"
        
        for handle, channel_id in CHANNELS.items():
            request = youtube.channels().list(
                part="statistics",
                id=channel_id
            )
            response = request.execute()
            
            if 'items' in response and len(response['items']) > 0:
                stats = response['items'][0]['statistics']
                subs = int(stats.get('subscriberCount', 0))
                views = int(stats.get('viewCount', 0))
                videos = int(stats.get('videoCount', 0))
                
                report += f"[ {handle} ]\n"
                report += f"- 👥 구독자 수: {subs:,}명\n"
                report += f"- 👁️ 총 조회수: {views:,}회\n"
                report += f"- 🎬 업로드 영상: {videos}개\n\n"
            else:
                report += f"[ {handle} ]\n- ⚠️ 채널 정보를 찾을 수 없습니다. (채널 ID 확인 필요)\n\n"
                
        return report
        
    except Exception as e:
        return f"⚠️ 유튜브 API 호출 실패: {str(e)}"
