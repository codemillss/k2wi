import os
import sys
import json
import re
import torch
from diffusers import DiffusionPipeline

# (선택 사항) ollama 종료
import subprocess
subprocess.run('sudo pkill -f ollama', shell=True, check=False)

# 🔹 받은 프롬프트 리스트 파싱
args = json.loads(sys.argv[1])

if isinstance(args, dict):
    recipe_name = args["name"].strip().replace(" ", "_")
    prompts = args["prompts"]

# 리스트만 전달된 경우 (기존 방식 유지용)
elif isinstance(args, list):
    recipe_name = "recipe"  # 기본 이름
    prompts = args

else:
    raise ValueError("입력값은 dict 또는 list여야 합니다.")

# 🔹 images 폴더 내 새 숫자 폴더 만들기
base_dir = "images"
os.makedirs(base_dir, exist_ok=True)

existing_ids = [int(name) for name in os.listdir(base_dir) if name.isdigit()]
new_id = max(existing_ids) + 1 if existing_ids else 1

output_dir = os.path.join(base_dir, str(new_id))
os.makedirs(output_dir, exist_ok=True)

# 🔹 모델 불러오기
model_id = "stabilityai/stable-diffusion-xl-base-1.0"
pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# 🔹 프롬프트 본문 추출 함수
def extract_prompt_text(prompt_block: str) -> str:
    match = re.search(r'\*\*프롬프트:\*\*\n\n"(.*?)"', prompt_block, re.DOTALL)
    return match.group(1).strip() if match else prompt_block.strip()

# 🔹 프롬프트별 이미지 생성
for idx, block in enumerate(prompts):
    prompt_text = extract_prompt_text(block)

    image = pipe(
        prompt=prompt_text,
        guidance_scale=7.5,
        num_inference_steps=50 #50으로 바꾸기
    ).images[0]

    filename = f"{recipe_name}_{idx+1}.png"
    save_path = os.path.join(output_dir, filename)
    image.save(save_path)
    print(f"✅ 이미지 저장 완료: {save_path}")
