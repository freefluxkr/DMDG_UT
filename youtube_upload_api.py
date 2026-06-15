import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    print("📋 [당목담글 비서: 페기] 유튜브 업로드 모듈 시작!")
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "C:\\Users\\tuesv\\Documents\\DMDG_UT\\client_secret.json"

    # Get credentials and create an API client
    try:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        print("✅ 인증 완료: 유튜브 API 연동 성공!")
    except Exception as e:
        print(f"⚠️ 인증 실패 또는 client_secret.json 없음: {e}")
        return

    # 업로드 요청 세팅 (실제 업로드는 막아둠 - 테스트 모드)
    request_body = {
        "snippet": {
            "categoryId": "1",
            "title": "[Day 001] 당글마을의 탄생! 자음과 모음이 만나다✨",
            "description": "아기자기한 툰 셰이딩으로 구현된 24자모의 당글마을 구축기! 통통 튀는 효과음과 함께 감상하세요.",
            "tags": ["당목담글", "애니메이션", "툰셰이딩", "카툰렌더링", "ASMR"]
        },
        "status": {
            "privacyStatus": "private" # 최초 업로드는 비공개
        }
    }

    # 실제 mp4 파일이 생성되면 아래 주석 해제하여 업로드
    """
    media_file = googleapiclient.http.MediaFileUpload('C:\\Users\\tuesv\\Documents\\DMDG_UT\\day001_village_scene.mp4')
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )
    response = request.execute()
    print("🎉 업로드 완료! 영상 ID:", response['id'])
    """
    print("✅ 준비 완료: 영상이 렌더링되면 즉시 업로드 가능한 상태입니다!")

if __name__ == "__main__":
    main()
