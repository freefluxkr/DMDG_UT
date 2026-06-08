import subprocess

url = "https://www.reddit.com/r/korea/hot.json?limit=5"
print("Fetching raw output from curl...")

try:
    result = subprocess.run(
        ["curl", "-i", "-s", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", url],
        capture_output=True,
        check=True
    )
    # Decode as utf-8 ignoring errors
    raw_out = result.stdout.decode('utf-8', errors='ignore')
    print("--- FIRST 500 CHARACTERS ---")
    print(raw_out[:500])
except Exception as e:
    print("Error:", e)
