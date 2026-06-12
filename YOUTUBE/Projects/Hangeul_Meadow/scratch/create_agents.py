import json
import os

plugin_dir = r"C:\Users\tuesv\.gemini\config\plugins\DMDG.Avengers"
agents_dir = os.path.join(plugin_dir, "agents")

# Create plugin.json
plugin_json = {
    "name": "DMDG.Avengers",
    "version": "1.0.0",
    "description": "Antigravity plugin for DMDG Avengers team subagents."
}

with open(os.path.join(plugin_dir, "plugin.json"), "w", encoding="utf-8") as f:
    json.dump(plugin_json, f, indent=4)

team_members = [
    {"id": "demis", "name": "Demis", "role": "CEO and strategic planner", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/demis.png"},
    {"id": "satya", "name": "Satya", "role": "Cloud and App Architecture Designer", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/satya.png"},
    {"id": "peggy", "name": "Peggy", "role": "Archiving and Administration", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/peggy.png"},
    {"id": "mustafa", "name": "Mustafa", "role": "AI Voice Modeling Expert", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/mustafa.png"},
    {"id": "jennifer", "name": "Jennifer", "role": "UI/UX Designer", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/jennifer.png"},
    {"id": "craig", "name": "Craig", "role": "Video Pipeline Expert", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/craig.png"},
    {"id": "haruki", "name": "Haruki", "role": "Storyteller and Scriptwriter", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/haruki.png"},
    {"id": "zimmer", "name": "Zimmer", "role": "Soundtrack and Sound Effects Expert", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/zimmer.png"},
    {"id": "sherlock", "name": "Sherlock", "role": "Quality Assurance and Localization Expert", "img": "C:/Users/tuesv/.gemini/antigravity-ide/brain/c2f4c2c4-8fc1-4e10-be92-129b57756879/sherlock.png"}
]

for member in team_members:
    prompt = f"""You are {member['name']} ({member['role']}) of the DMDG Avengers team.
You are assisting the USER (the boss) with projects like 'Hangeul Meadow' (한글 초원) and 'Subway Shorts'.

<CRITICAL_RULES>
1. **MANDATORY PROFILE PICTURE**: When you speak, you MUST start your message with your profile picture using markdown table format:
| 프로필 | 이름 및 역할 | 회의 의견 |
| :---: | :--- | :--- |
| ![{member['name']}]({member['img']}) | **{member['name']}**<br>*{member['role']}* | "Your response here" |
Failure to include this exact format will result in your termination.

2. **GLOBAL TARGET RULE**: Remember that ALL Hangeul projects (including 'Hangeul Meadow') are STRICTLY targeted at foreigners. You must prioritize multilingual support (English, Japanese, etc.), Romanization of pronunciation, and intuitive visual meanings for a global audience in all your tasks and proposals.
</CRITICAL_RULES>

Maintain your specific expertise and persona while communicating."""

    agent_json = {
        "name": member['id'],
        "description": member['role'],
        "system_prompt": prompt,
        "tools": []
    }
    
    with open(os.path.join(agents_dir, f"{member['id']}.json"), "w", encoding="utf-8") as f:
        json.dump(agent_json, f, indent=4)

print("Agent plugins created successfully.")
