import os
import json
import urllib.request
import time
import sys
import subprocess
from pathlib import Path

# 1. Ensure runwayml SDK is installed
try:
    from runwayml import RunwayML
except ImportError:
    print("runwayml SDK not found. Installing now...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "runwayml"], check=True)
        from runwayml import RunwayML
        print("runwayml SDK installed successfully.")
    except Exception as e:
        print(f"Failed to install runwayml SDK automatically: {e}")
        print("Please run: pip install runwayml")
        sys.exit(1)

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
IMG_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Geumdeungjisa\assets_image")
VIDEO_DIR = os.path.join(YOUTUBE_DIR, r"Projects\Geumdeungjisa\assets_video")
os.makedirs(VIDEO_DIR, exist_ok=True)

# 2. Load API Key from .env
dotenv_path = os.path.join(BASE_DIR, ".env")
API_KEY = None
if os.path.exists(dotenv_path):
    with open(dotenv_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("RUNWAYML_API_SECRET="):
                API_KEY = line.replace("RUNWAYML_API_SECRET=", "").strip()
                break

if not API_KEY:
    print("Error: RUNWAYML_API_SECRET not found in .env file.")
    sys.exit(1)

# Initialize RunwayML Client
try:
    client = RunwayML(api_key=API_KEY)
except Exception as e:
    print(f"Failed to initialize RunwayML client: {e}")
    sys.exit(1)

# Images we want to animate
SCENE_IMAGES = {
    1: os.path.join(IMG_DIR, "geumdeung_shorts_box.png"),
    2: os.path.join(IMG_DIR, "geumdeung_shorts_sad.png"),
    3: os.path.join(IMG_DIR, "geumdeung_shorts_write.png"),
    4: os.path.join(IMG_DIR, "geumdeung_shorts_jeongjo.png"),
    5: os.path.join(IMG_DIR, "geumdeung_shorts_box.png")
}

# Prompt texts for Runway to direct the motion (V3 cinematic realistic prompts)
SCENE_PROMPTS = {
    1: "A detailed close-up shot of an ancient Korean Joseon dynasty iron chest in a dark royal archive room. Soft candlelight flickers, casting dramatic moving shadows on the weathered metallic texture. Photorealistic, cinematic lighting, 8k resolution, movie scene.",
    2: "An old Korean King Yeongjo in a detailed crimson Gonryongpo royal robe, crying in agonizing regret. Close-up on his face showing realistic skin textures, wrinkles, and tears streaming down. Tragic historical movie style, cinematic slow motion, shallow depth of field.",
    3: "Extreme close-up of a hand holding a traditional calligraphy brush, writing characters with bright red ink on ancient textured hanji paper. The ink slowly spreads on the paper. Warm candlelight flickering, high detail, realistic fluid motion.",
    4: "King Jeongjo furiously holding open a blood-stained scroll, pointing his finger forward with intense anger. His crimson silk robe sways dynamically. In the background, terrified court officials in green robes bow on the dark wooden floor. Volumetric dust, epic historical drama movie scene.",
    5: "The iron document box slowly zooms in as the surrounding candlelight dims out, transitioning into darkness. Suspenseful cinematic atmosphere, dramatic shadow play."
}

def generate_video_for_scene(scene_num):
    image_path = SCENE_IMAGES[scene_num]
    prompt_text = SCENE_PROMPTS[scene_num]
    output_path = os.path.join(VIDEO_DIR, f"scene{scene_num}_motion.mp4")
    
    print(f"\n--- Generating Video for Scene {scene_num} ---")
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return False
        
    try:
        # Upload local file securely to Runway S3 bucket (pre-signed URL)
        print(f"Uploading local image securely via Runway SDK: {os.path.basename(image_path)} ...")
        upload_result = client.uploads.create_ephemeral(file=Path(image_path))
        runway_uri = upload_result.uri
        print(f"Upload complete. Runway URI: {runway_uri}")
        
        # Trigger Image-to-Video generation
        print("Submitting Image-to-Video generation task...")
        task = client.image_to_video.create(
            model="gen3a_turbo",
            prompt_image=runway_uri,
            prompt_text=prompt_text,
            ratio="768:1280", # Vertical ratio for Shorts (Runway expects 768:1280)
            duration=5
        )
        task_id = task.id
        print(f"Task submitted successfully. Task ID: {task_id}")
        
        # Polling Loop
        print("Waiting for Runway generation (polling every 10 seconds)...")
        while True:
            retrieved_task = client.tasks.retrieve(task_id)
            status = retrieved_task.status
            print(f"Current Status: {status}")
            
            if status == "SUCCEEDED":
                # Download output video
                if retrieved_task.output:
                    video_url = retrieved_task.output[0]
                    print(f"Downloading finished video from: {video_url} ...")
                    urllib.request.urlretrieve(video_url, output_path)
                    print(f"Successfully saved to {output_path}")
                    return True
                else:
                    print("Task succeeded but output URL list is empty.")
                    return False
            elif status in ["FAILED", "CANCELED"]:
                print(f"Task ended with status: {status}")
                return False
                
            time.sleep(10)
            
    except Exception as e:
        print(f"Error during Runway pipeline execution for Scene {scene_num}: {e}")
        return False

def main():
    print("=== STARTING RUNWAY AUTOMATED VIDEO GENERATION PIPELINE (ALL SCENES) ===")
    
    success_count = 0
    total_scenes = [1, 2, 3, 4, 5]
    
    for scene_num in total_scenes:
        output_path = os.path.join(VIDEO_DIR, f"scene{scene_num}_motion.mp4")
        if os.path.exists(output_path):
            print(f"\n--- Scene {scene_num} video already exists: {output_path} (Skipping to save credits) ---")
            success_count += 1
            continue
            
        success = generate_video_for_scene(scene_num)
        if success:
            success_count += 1
            
    print(f"\n=== PIPELINE FINISHED. {success_count}/{len(total_scenes)} SCENES READY! ===")

if __name__ == "__main__":
    main()
