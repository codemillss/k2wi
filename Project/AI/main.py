import os
import sys
import subprocess
import pandas as pd
import json
from recipe_image_pipeline import recipe_to_image_prompts

SD_SCRIPT = "/home/ubuntu/work/model/stable-diffusion-xl-base-1.0.py"

# CSV → 시연
if __name__ == "__main__":
    df = pd.read_csv("/home/ubuntu/work/data/temp.csv")

    for idx, row in df.iterrows():
        recipe_name = row["name"].strip().replace(" ", "_")
        steps_raw = eval(row["steps"])  # CSV 에 list 형태로 저장된 경우

        prompts = recipe_to_image_prompts(steps_raw)
        for i, p in enumerate(prompts, 1):
            print(f"🖼️ Step {i}: {p}")

        # ——— Stable‑Diffusion 호출 ———
        payload = json.dumps({"name": recipe_name, "prompts": prompts})
        subprocess.run(["python3", SD_SCRIPT, payload], check=True)