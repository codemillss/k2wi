import sys
import json
import re
import torch
from diffusers import FluxPipeline

# (선택 사항) ollama 종료
import subprocess
subprocess.run('sudo pkill -f ollama', shell=True, check=False)

# 🔹 받은 프롬프트 리스트 파싱
prompts = json.loads(sys.argv[1])  # 문자열로 된 JSON 리스트 → Python 리스트로 변환

# 🔹 모델 불러오기
model_id = "black-forest-labs/FLUX.1-dev"
pipe = FluxPipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()
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
        num_inference_steps=50,
        max_sequence_length=512,
    generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]

    image.save(f"./img_dir/stable-diffusion-xl-base-1.0/sd-image-step{idx+1}.png")
    print(f"✅ 이미지 저장 완료: sd-image-step{idx+1}.png")
