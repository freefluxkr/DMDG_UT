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
        print("Please run: pip install runwayml")
        sys.exit(1)

BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
YOUTUBE_DIR = os.path.join(BASE_DIR, "YOUTUBE")
PROJECT_DIR = os.path.join(YOUTUBE_DIR, r"Projects\TempleFood")
IMG_DIR = os.path.join(PROJECT_DIR, "assets_image")
VIDEO_DIR = os.path.join(PROJECT_DIR, "assets_video")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# Sources of the generated images in the brain folder (FIXED versions using character sheet reference images)
BRAIN_DIR = r"C:\Users\user\.gemini\antigravity-ide\brain\d548359c-b1d4-4fb5-a3f4-57d851eaacc1"
SOURCE_IMAGES = {
    1: os.path.join(BRAIN_DIR, "temple_food_scene1_fixed_1780897001599.png"),
    2: os.path.join(BRAIN_DIR, "temple_food_scene2_fixed_1780897021265.png"),
    3: os.path.join(BRAIN_DIR, "temple_food_scene3_fixed_1780897041031.png"),
    4: os.path.join(BRAIN_DIR, "temple_food_scene4_fixed_1780897057488.png"),
    5: os.path.join(BRAIN_DIR, "temple_food_scene5_fixed_1780897078049.png")
}

# Destinations
SCENE_IMAGES = {
    1: os.path.join(IMG_DIR, "scene1.png"),
    2: os.path.join(IMG_DIR, "scene2.png"),
    3: os.path.join(IMG_DIR, "scene3.png"),
    4: os.path.join(IMG_DIR, "scene4.png"),
    5: os.path.join(IMG_DIR, "scene5.png")
}

# Copy files (force overwrite to replace old ones)
print("Copying base images to project directory...")
for num in range(1, 6):
    src = SOURCE_IMAGES[num]
    dest = SCENE_IMAGES[num]
    if os.path.exists(src):
        shutil.copy2(src, dest)
        print(f"Copied Scene {num} -> {dest}")
    else:
        print(f"Warning: Source image not found for Scene {num}: {src}")

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

# Prompt texts for Runway to direct the motion
SCENE_PROMPTS = {
    1: "A cinematic, slow-motion shot of a misty early morning at a traditional Korean Hanok temple deep in the mountains. Wind chimes gently sway. Volumetric lighting, mist rising, photorealistic, 8k resolution, slow panning.",
    2: "Close-up of rugged hands putting fresh green wild herbs into a large boiling cast-iron pot over a wood-fire stove. Next to the stove, a cute small mythical Haetae creature with big expressive eyes watches with curiosity. Warm lighting, steam rising, highly detailed.",
    3: "Close-up of thick shiitake mushrooms sizzling on a flat iron pan over red charcoal. A cute small Haetae creature Duffy is nearby sniffing the savory aroma. A thick, dark brown soy-sauce glaze is poured over, bubbling and caramelizing.",
    4: "A clay pot boiling with yellow pumpkin broth, tofu cubes, and dough balls. A cute small Haetae creature Duffy sits snugly by the warm firewood stove. Cozy temple kitchen atmosphere, steam rising, photorealistic.",
    5: "A wide shot of a peaceful Korean temple veranda. A middle-aged Korean man Seo-ssi and a cute small Haetae creature Duffy sit side-by-side facing misty mountains, quietly sharing a simple meal from wooden bowls. Golden hour sunlight, serene, zen atmosphere."
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
    print("=== STARTING TEMPLE FOOD VIDEO GENERATION PIPELINE ===")
    
    success_count = 0
    total_scenes = [1, 2, 3, 4, 5]
    
    for scene_num in total_scenes:
        output_path = os.path.join(VIDEO_DIR, f"scene{scene_num}_motion.mp4")
        # Delete existing video to force regeneration with the new correct characters
        if os.path.exists(output_path):
            os.remove(output_path)
            
        success = generate_video_for_scene(scene_num)
        if success:
            success_count += 1
            
    print(f"\n=== PIPELINE FINISHED. {success_count}/{len(total_scenes)} SCENES READY! ===")

if __name__ == "__main__":
    main()
