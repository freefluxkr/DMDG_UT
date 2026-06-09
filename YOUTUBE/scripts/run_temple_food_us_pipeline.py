import os
import shutil
import json
import urllib.request
import time
import sys
import subprocess
from pathlib import Path

# Ensure runwayml SDK is installed
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
        sys.exit(1)

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
PROJECT_DIR = os.path.join(YOUTUBE_DIR, r"Projects\TempleFoodUS")
IMG_DIR = os.path.join(PROJECT_DIR, "assets_image")
VIDEO_DIR = os.path.join(PROJECT_DIR, "assets_video")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# Load API Key from .env
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

# Prompt texts for Runway to direct the motion (16:9 widescreen edition)
SCENE_PROMPTS = {
    1: "A cinematic widescreen 16:9 shot. Duffy sits happily in the shopping cart pointing its paw at fresh kale, while Seo-ssi pushes the cart in a bright organic store. Gentle camera pan.",
    2: "Close-up 16:9 shot. Seo-ssi's rugged hands hold a butternut squash and green kale. Duffy raises its paws in joy inside the cart, tail wagging slowly.",
    3: "A medium close-up 16:9 widescreen shot. Seo-ssi carefully trims green kale leaves on a cutting board, while Duffy wearing a tiny apron stacks them neatly into a basket.",
    4: "A 16:9 widescreen shot. Duffy wearing a tiny apron peels the outer leaves of baby Brussels sprouts, while Seo-ssi trims the ends on a clean counter.",
    5: "Close-up 16:9 shot. Seo-ssi's hands peel the skin of a butternut squash, while Duffy sits next to a pot, looking up hungrily. Squash cubes are arranged nearby.",
    6: "A dynamic 16:9 widescreen shot. Steam rises from pots on the stove. Seo-ssi blanches green kale, while Duffy stands on a stool holding a spoon, looking inside the pot.",
    7: "A cinematic 16:9 shot. Bobby and Heo Yong-joon sit at a table overlooking a garden, looking at plates of temple food. Seo-ssi and Duffy smile behind them.",
    8: "A medium close-up 16:9 shot. Bobby eats yellow soup and gives a thumbs-up. Heo Yong-joon smiles eating kale namul. Duffy wags its tail, leaning on Heo Yong-joon's arm."
}

def generate_video_for_scene(scene_num):
    image_path = os.path.join(IMG_DIR, f"scene{scene_num}.png")
    prompt_text = SCENE_PROMPTS[scene_num]
    output_path = os.path.join(VIDEO_DIR, f"scene{scene_num}_motion.mp4")
    
    print(f"\n--- Generating Video for Scene {scene_num} ---")
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return False
        
    try:
        print(f"Uploading local image securely via Runway SDK: {os.path.basename(image_path)} ...")
        upload_result = client.uploads.create_ephemeral(file=Path(image_path))
        runway_uri = upload_result.uri
        print(f"Upload complete. Runway URI: {runway_uri}")
        
        print("Submitting Image-to-Video generation task...")
        task = client.image_to_video.create(
            model="gen3a_turbo",
            prompt_image=runway_uri,
            prompt_text=prompt_text,
            ratio="1280:768", # Widescreen 16:9 ratio
            duration=5
        )
        task_id = task.id
        print(f"Task submitted successfully. Task ID: {task_id}")
        
        print("Waiting for Runway generation (polling every 10 seconds)...")
        while True:
            retrieved_task = client.tasks.retrieve(task_id)
            status = retrieved_task.status
            print(f"Current Status: {status}")
            
            if status == "SUCCEEDED":
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
    print("=== STARTING TEMPLE FOOD US KITCHEN 16:9 VIDEO PIPELINE ===")
    
    success_count = 0
    total_scenes = [1, 2, 3, 4, 5, 6, 7, 8]
    
    for scene_num in total_scenes:
        output_path = os.path.join(VIDEO_DIR, f"scene{scene_num}_motion.mp4")
        if os.path.exists(output_path):
            os.remove(output_path)
            
        success = generate_video_for_scene(scene_num)
        if success:
            success_count += 1
            
    print(f"\n=== PIPELINE FINISHED. {success_count}/{len(total_scenes)} SCENES READY! ===")

if __name__ == "__main__":
    main()
