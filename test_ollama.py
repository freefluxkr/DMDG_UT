import json
import urllib.request
import urllib.error
import os

CONFIG_PATH = 'antigravity.config.json'

def test_ollama():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        local_model_config = config.get('models', {}).get('local', {})
        base_url = local_model_config.get('baseUrl', 'http://localhost:11434')
        model = local_model_config.get('model', 'gemma2:2b')
        
        print(f"[*] 테스트 시작: 로컬 Ollama 모델 ({model}) @ {base_url}")
        
        # OpenAI 호환 엔드포인트 테스트
        endpoint = f"{base_url}/v1/chat/completions"
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": "안녕하세요! 테스트 중입니다. 짧게 인사해주세요."}],
            "temperature": local_model_config.get('temperature', 0.1),
            "max_tokens": 50
        }
        
        req = urllib.request.Request(endpoint, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        print("[*] OpenAI 호환 API로 요청을 전송합니다...")
        response = urllib.request.urlopen(req, timeout=15)
        result = json.loads(response.read().decode('utf-8'))
        
        print("\n[+] 응답 성공!")
        print("-" * 40)
        print(result['choices'][0]['message']['content'].strip())
        print("-" * 40)
        print("[+] OpenAI 호환 엔드포인트 테스트가 완료되었습니다.")
        
    except urllib.error.URLError as e:
        print(f"[-] 연결 실패: Ollama 서버가 {base_url} 에서 실행 중인지 확인해주세요.")
        print(f"[-] 상세 에러: {e.reason}")
        
        print("\n[*] Ollama 기본 API(/api/generate)로 재시도합니다...")
        try:
             endpoint = f"{base_url}/api/generate"
             data = {
                 "model": model,
                 "prompt": "안녕하세요! 테스트 중입니다. 짧게 인사해주세요.",
                 "stream": False
             }
             req = urllib.request.Request(endpoint, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
             response = urllib.request.urlopen(req, timeout=15)
             result = json.loads(response.read().decode('utf-8'))
             print("\n[+] 응답 성공!")
             print("-" * 40)
             print(result['response'].strip())
             print("-" * 40)
             print("[+] Ollama 기본 엔드포인트 테스트가 완료되었습니다.")
        except Exception as e2:
             print(f"[-] 기본 엔드포인트 요청도 실패했습니다: {e2}")
    except Exception as e:
        print(f"[-] 에러 발생: {e}")

if __name__ == '__main__':
    test_ollama()
