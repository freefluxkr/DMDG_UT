import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Analytics API의 읽기 전용 권한 스코프
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

def get_authenticated_service():
    creds = None
    # token.json 파일에 이전에 인증된 정보가 있는지 확인
    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')
    client_secret_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client_secret.json')
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    # 유효한 인증 정보가 없으면 새로 로그인 유도
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            # 로컬 서버를 띄워서 구글 로그인 콜백을 받음
            creds = flow.run_local_server(port=0)
            
        # 토큰을 파일로 저장하여 다음에는 로그인 안해도 되게 함
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    return build('youtubeAnalytics', 'v2', credentials=creds)

def fetch_analytics_report():
    try:
        youtube_analytics = get_authenticated_service()
        
        # 오늘 기준으로 30일 전부터 3일 전까지 데이터 (가장 최근 데이터는 2~3일 지연됨)
        end_date = (datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
        start_date = (datetime.date.today() - datetime.timedelta(days=33)).strftime('%Y-%m-%d')
        
        # 1. 시청자 성별/연령
        demographics_response = youtube_analytics.reports().query(
            ids='channel==MINE',
            startDate=start_date,
            endDate=end_date,
            metrics='viewerPercentage',
            dimensions='ageGroup,gender',
            sort='-viewerPercentage'
        ).execute()
        
        # 2. 유입 경로 (Traffic Sources)
        traffic_response = youtube_analytics.reports().query(
            ids='channel==MINE',
            startDate=start_date,
            endDate=end_date,
            metrics='views,estimatedMinutesWatched',
            dimensions='insightTrafficSourceType',
            sort='-views',
            maxResults=5
        ).execute()
        
        # 리포트 조립
        report_text = "[유튜브 심층 애널리틱스 분석]\n\n"
        
        gender_map = {'MALE': '남성', 'FEMALE': '여성', 'USER_SPECIFIED': '기타'}
        report_text += "■ 주요 시청자 층 (연령/성별)\n"
        if 'rows' in demographics_response and demographics_response['rows']:
            for row in demographics_response['rows'][:3]:
                gender_kr = gender_map.get(row[1].upper(), row[1].upper())
                report_text += f"- {gender_kr} ({row[0][3:]}대): {row[2]:.1f}%\n"
        else:
            report_text += "- 데이터 없음\n"
            
        source_map = {
            'SHORTS': '쇼츠 피드',
            'YT_SEARCH': '유튜브 검색',
            'YT_CHANNEL': '채널 페이지',
            'YT_OTHER_PAGE': '기타 유튜브 페이지',
            'NO_LINK_OTHER': '알 수 없는 외부 유입',
            'SUBSCRIBER': '구독 피드',
            'RELATED_VIDEO': '추천 동영상',
            'EXT_URL': '외부 링크',
            'PLAYLIST': '재생목록'
        }
        report_text += "\n■ 주요 유입 경로 (Traffic Sources)\n"
        if 'rows' in traffic_response and traffic_response['rows']:
            for row in traffic_response['rows']:
                source_raw = row[0]
                source_kr = source_map.get(source_raw, source_raw)
                views = row[1]
                report_text += f"- {source_kr}: {views}회 시청\n"
        else:
            report_text += "- 데이터 없음\n"
            
        return report_text
        
    except Exception as e:
        return f"[애널리틱스 오류] {str(e)}"

if __name__ == '__main__':
    print("인증 및 통계 추출 테스트를 시작합니다...")
    print(fetch_analytics_report())
