import os
import shutil
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
        sys.exit(1)

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
PROJECT_DIR = os.path.join(YOUTUBE_DIR, r"Projects\TempleFoodUS")
IMG_DIR = os.path.join(PROJECT_DIR, "assets_image")
VIDEO_DIR = os.path.join(PROJECT_DIR, "assets_video")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# Sources of the generated images in the brain folder
BRAIN_DIR = r"C:\Users\user\.gemini\antigravity-ide\brain\d548359c-b1d4-4fb5-a3f4-57d851eaacc1"
SOURCE_IMAGES = {
    1: os.path.join(BRAIN_DIR, "temple_food_us_scene1_fixed_1780897563743.png"),
    2: os.path.join(BRAIN_DIR, "temple_food_us_scene2_fixed_1780897578833.png"),
    3: os.path.join(BRAIN_DIR, "temple_food_us_scene3_fixed_1780897592443.png"),
    4: os.path.join(BRAIN_DIR, "temple_food_scene4_fixed_1780897057488.png"), # Fallback (Duffy by stove)
    5: os.path.join(BRAIN_DIR, "temple_food_scene5_fixed_1780897078049.png")  # Fallback (Duffy and Seo-ssi veranda)
}

# Destinations
SCENE_IMAGES = {
    1: os.path.join(IMG_DIR, "scene1.png"),
    2: os.path.join(IMG_DIR, "scene2.png"),
    3: os.path.join(IMG_DIR, "scene3.png"),
    4: os.path.join(IMG_DIR, "scene4.png"),
    5: os.path.join(IMG_DIR, "scene5.png")
}

# Copy files
print("Copying base images to project directory...")
for num in range(1, 6):
    src = SOURCE_IMAGES[num]
    dest = SCENE_IMAGES[num]
    if os.path.exists(src):
        shutil.copy2(src, dest)
        print(f"Copied Scene {num} -> {dest}")
    else:
        print(f"Warning: Source image not found for Scene {num}: {src}")

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

# Prompt texts for Runway to direct the motion (Chef Duffy version)
SCENE_PROMPTS = {
    1: "A cinematic, vertical 9:16 shot of a bright organic supermarket. A cute small Haetae mascot creature Duffy happily sits in the shopping cart, using its paw to pick up fresh green kale. Natural lighting, commercial film look.",
    2: "Top-down vertical 9:16 shot of a modern kitchen island. The cute Haetae creature Duffy wearing a small apron sits on the counter, using its paws to mix blanched kale in a bowl while perilla oil is poured. Natural sunlight.",
    3: "Close-up of Brussels sprouts searing in a black cast-iron skillet. The cute Haetae creature Duffy wearing a small apron holds a small wooden spatula to stir-fry the sprouts. Ginger-soy glaze bubbles and sizzles.",
    4: "Vibrant yellow butternut squash soup bubbling in a pot. The cute Haetae creature Duffy stir-fries with a wooden ladle, sniffing the warm sweet aroma happily. Cozy kitchen lighting.",
    5: "A wide shot of a dining room. The cute Haetae creature Duffy sits on a tall chair, holding a spoon and happily eating temple food. Golden hour sunlight, serene atmosphere."
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
        print(f"Uploading local image securely via Runway SDK: {os.path.basename(image_path)} ...")
        upload_result = client.uploads.create_ephemeral(file=Path(image_path))
        runway_uri = upload_result.uri
        print(f"Upload complete. Runway URI: {runway_uri}")
        
        print("Submitting Image-to-Video generation task...")
        task = client.image_to_video.create(
            model="gen3a_turbo",
            prompt_image=runway_uri,
            prompt_text=prompt_text,
            ratio="768:1280", # Vertical ratio for Shorts
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
    print("=== STARTING TEMPLE FOOD US KITCHEN VIDEO GENERATION PIPELINE ===")
    
    success_count = 0
    total_scenes = [1, 2, 3, 4, 5]
    
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
