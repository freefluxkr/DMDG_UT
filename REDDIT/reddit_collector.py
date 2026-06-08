import os
import json
import subprocess
import re
from datetime import datetime

project_dir = r"c:\Users\user\Documents\DMDG_UT"
kb_dir = os.path.join(project_dir, "AI_Knowledge_Base")
reddit_kb_dir = os.path.join(kb_dir, "reddit")

# Subreddits to fetch
subreddits = ["korea", "korean", "LocalLLaMA"]

def clean_filename(title):
    clean = re.sub(r'[\\/*?:"<>|]', "", title)
    return clean[:80].strip()

def fetch_subreddit_hot_curl(sub):
    url = f"https://www.reddit.com/r/{sub}/hot.json?limit=5"
    print(f"Running curl for r/{sub}...")
    try:
        # Use Windows built-in curl to bypass python urllib TLS fingerprint blocks
        result = subprocess.run(
            ["curl", "-s", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", url],
            capture_output=True,
            check=True
        )
        # Decode as utf-8 (ignoring decode errors) to prevent cp949 encoding errors on Korean Windows
        stdout_str = result.stdout.decode("utf-8", errors="ignore")
        data = json.loads(stdout_str)
        return data.get("data", {}).get("children", [])
    except Exception as e:
        print(f"❌ Failed to fetch r/{sub}: {e}")
        return []

def save_post_to_md(sub, post_data):
    title = post_data.get("title", "Untitled")
    author = post_data.get("author", "unknown")
    score = post_data.get("score", 0)
    num_comments = post_data.get("num_comments", 0)
    permalink = f"https://www.reddit.com{post_data.get('permalink')}"
    selftext = post_data.get("selftext", "")
    created_utc = post_data.get("created_utc", 0)
    created_time = datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
    
    filename = f"reddit_{sub}_{clean_filename(title)}.md"
    file_path = os.path.join(reddit_kb_dir, filename)
    
    md_content = f"""# [{sub}] {title}

| 항목 | 내용 |
|------|------|
| **게시판** | r/{sub} |
| **작성자** | u/{author} |
| **추천수(Score)** | {score} |
| **댓글수** | {num_comments} |
| **수집일자** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| **원문 링크** | [Reddit Link]({permalink}) |

---

## 📝 본문 내용

{selftext if selftext.strip() else "*[이미지 또는 외부 링크 글입니다]*"}

---

## 🧠 AI 에이전트 분석 요약 (For YouTube & RAG)
- **키워드**: #reddit, #{sub}, #{author}
- **기획 영감**: 이 글에 언급된 트렌드나 외국인들의 반응은 [[회의록/008_shorts_script_subway_manners|지하철 쇼츠 대본]] 이나 [[회의록/viral_content_proposal|바이럴 제안]]에 글로벌 피드백 자료로 유용하게 참조될 수 있습니다.
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved post: {filename}")

def main():
    if not os.path.exists(reddit_kb_dir):
        os.makedirs(reddit_kb_dir)
        print(f"Created Reddit Knowledge Base folder at: {reddit_kb_dir}")
        
    print("--- Reddit Trend Collector Starting (via Curl) ---")
    for sub in subreddits:
        posts = fetch_subreddit_hot_curl(sub)
        
        saved_count = 0
        for post in posts:
            post_data = post.get("data", {})
            if post_data.get("stickied"):
                continue
                
            save_post_to_md(sub, post_data)
            saved_count += 1
            if saved_count >= 3:
                break
                
    print("\nReddit Collection Completed Successfully!")

if __name__ == "__main__":
    main()
