import bpy
import math
import random
import os

# 당글마을 전체 자음과 모음
CONSONANTS = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
VOWELS = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ']
ALL_LETTERS = CONSONANTS + VOWELS

def setup_scene():
    # 기본 큐브 삭제
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # 조명 추가 (Sun)
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.data.angle = math.radians(10) # 부드러운 그림자
    
    # 카메라 추가 (쇼츠 뷰를 위한 화각 세팅)
    bpy.ops.object.camera_add(location=(0, -25, 15), rotation=(math.radians(60), 0, 0))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera

def create_clay_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        if 'Roughness' in bsdf.inputs:
            bsdf.inputs['Roughness'].default_value = 0.8
    return mat

def create_text_object(char, name, location, material):
    bpy.ops.object.text_add(location=location)
    text_obj = bpy.context.active_object
    text_obj.name = name
    text_obj.data.body = char
    
    # 폰트 굵게 및 베벨(찰흙 느낌)
    text_obj.data.extrude = 0.4
    text_obj.data.bevel_depth = 0.1
    text_obj.data.bevel_resolution = 5
    
    # 윈도우 기본 맑은 고딕 폰트 적용 (한글 깨짐 방지)
    font_path = "C:\\Windows\\Fonts\\malgunbd.ttf"  # 맑은 고딕 볼드
    if not os.path.exists(font_path):
        font_path = "C:\\Windows\\Fonts\\malgun.ttf"
        
    if os.path.exists(font_path):
        fnt = bpy.data.fonts.load(font_path)
        text_obj.data.font = fnt
        
    text_obj.data.materials.append(material)
    
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    
    return text_obj

def build_dangeul_village():
    colors = [
        (0.2, 0.6, 0.8, 1), # Blue
        (0.8, 0.4, 0.1, 1), # Orange
        (0.2, 0.8, 0.4, 1), # Green
        (0.8, 0.2, 0.4, 1), # Red/Pink
        (0.9, 0.8, 0.2, 1)  # Yellow
    ]
    materials = [create_clay_material(f"Clay_{i}", c) for i, c in enumerate(colors)]
    
    objects = []
    
    # 1단계: 하늘에서 무작위로 떨어지는 24개 글자들
    for i, char in enumerate(ALL_LETTERS):
        mat = random.choice(materials)
        
        # 무작위 하늘 스폰 포인트
        start_x = random.uniform(-10, 10)
        start_y = random.uniform(-5, 15)
        start_z = random.uniform(10, 40)
        
        obj = create_text_object(char, f"Letter_{char}", (start_x, start_y, start_z), mat)
        
        # 대기 시간 (프레임 1 ~ 30 사이 랜덤 출발)
        start_frame = random.randint(1, 30)
        bpy.context.view_layer.update()
        obj.keyframe_insert(data_path="location", frame=1)
        obj.keyframe_insert(data_path="location", frame=start_frame)
        
        # 바닥 충돌 위치 계산
        ground_frame = start_frame + 20
        ground_x = start_x * 0.6
        ground_y = start_y * 0.6
        ground_z = 0.0
        
        obj.location = (ground_x, ground_y, ground_z)
        obj.rotation_euler = (math.radians(random.uniform(0, 360)), math.radians(random.uniform(0, 360)), math.radians(random.uniform(0, 360)))
        obj.keyframe_insert(data_path="location", frame=ground_frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=ground_frame)
        
        objects.append((obj, ground_x, ground_y))
        
    # 2단계: 클라이맥스 (모든 글자가 자석처럼 중앙으로 모여들어 돔 형태 구성)
    climax_frame = 100
    for i, (obj, g_x, g_y) in enumerate(objects):
        # 중앙 돔 배치를 위한 수학적 계산
        angle = (i / len(objects)) * math.pi * 4  # 소용돌이 형태
        radius = random.uniform(1.5, 6.0)
        
        final_x = math.cos(angle) * radius
        final_y = math.sin(angle) * radius
        final_z = random.uniform(0, 5.0) # 중앙 탑처럼 쌓임
        
        # 프레임 70부터 이동 시작
        obj.keyframe_insert(data_path="location", frame=70)
        obj.keyframe_insert(data_path="rotation_euler", frame=70)
        
        # 목적지 꽂히기
        obj.location = (final_x, final_y, final_z)
        obj.rotation_euler = (math.radians(90), 0, angle + math.radians(90)) # 세워서 둥글게 배치
        
        obj.keyframe_insert(data_path="location", frame=climax_frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=climax_frame)
        
        # 통통 튀는 애니메이션 (기본 Bezier 보간법 유지)

if __name__ == "__main__":
    setup_scene()
    build_dangeul_village()
    
    # 씬 저장 및 설정 (120프레임 = 5초)
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1920
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 120
    
    output_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "day001_village_scene.blend")
    bpy.ops.wm.save_as_mainfile(filepath=output_blend)
    print(f"✅ 24자모 당글마을 대규모 클러스터링 프로젝트가 저장되었습니다: {output_blend}")
