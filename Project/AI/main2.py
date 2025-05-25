import json
import subprocess
import pandas as pd
from PIL import Image
from ocr_utils import extract_text_from_image
from step_parser import parse_steps_with_llm
from prompt_generator import generate_image_prompts_from_steps

def full_recipe_to_image_prompts(input_data, input_type="text"):
    if input_type == "image":
        content = extract_text_from_image(input_data)  # 👉 str
        steps = parse_steps_with_llm(content)          # 👉 단계 분리 필요
    elif input_type == "text":
        if isinstance(input_data, list):
            steps = input_data  # 이미 분리된 단계
        elif isinstance(input_data, str):
            # 혹시 OCR 결과 형식이라면 이 경우도 파싱
            steps = parse_steps_with_llm(input_data)
        else:
            raise ValueError("텍스트 입력은 문자열 또는 문자열 리스트여야 합니다.")
    else:
        raise ValueError("input_type은 'text' 또는 'image'만 가능합니다.")

    prompts = generate_image_prompts_from_steps(steps)
    return prompts


def detect_input_type(data):
    if isinstance(data, str) or (isinstance(data, list) and all(isinstance(d, str) for d in data)):
        return "text"
    elif isinstance(data, Image.Image):
        return "image"
    else:
        raise ValueError("입력 형식이 올바르지 않습니다.")

if __name__ == "__main__":
    data = pd.read_csv("data/temp.csv")  # 또는 CSV, Parquet 등으로 교체
    # data = pd.read_csv("temple_recipe.csv")  # 또는 CSV, Parquet 등으로 교체

    for idx, row in data.iterrows():
        recipe_name = row["name"]
        raw_step_data = row["steps"]  # list or image

        input_type = detect_input_type(raw_step_data)
        print(f"\n📌 Processing: {recipe_name} ({idx}) [{input_type}]")

        try:
            prompts = full_recipe_to_image_prompts(raw_step_data, input_type=input_type)
            for i, p in enumerate(prompts, 1):
                print(f"🖼️ Step {i}:", p)

            subprocess.run([
                # "python3", "model/stable-diffusion-xl-base-1.0.py",
                "python3", "model/stable-diffusion-xl-base-1.0.py",

                json.dumps({
                    "name": recipe_name,
                    "prompts": prompts
                    })
                    ])
            
        except Exception as e:
            print(f"❌ Error processing '{recipe_name}' at index {idx}: {e}")
