# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# from fastapi.responses import JSONResponse
# import os
# import base64

# import subprocess
# import sys
# import json

# # sys.path.append(os.path.abspath('../work'))

# from ocr_utils import extract_text_from_image
# from step_parser import parse_steps_with_llm
# from prompt_generator import generate_image_prompts_from_steps
# from main import full_recipe_to_image_prompts
# from main import detect_input_type

# app = FastAPI()

# class ForMakeImage(BaseModel):
#     kimchi_num: int
#     kimchi_name: str
#     recipe_order: int
#     recipe_detail: str

    

# @app.get("/")
# def read_root():
#     return {"message": "Hello FastAPI!"}

# # @app.post("/MakeImage/")
# # async def create_image(ForMakeImage: List[ForMakeImage]):
    
# #     for item in ForMakeImage:
# #         print(item.kimchi_num, item.kimchi_name, item.recipe_order, item.recipe_detail)

# #     #받은 데이터를 통해 이미지를 만들고 난 후 데이터 전송
    
# #     return {"status": "✅ 데이터 잘 받았습니다", "count": len(ForMakeImage), "Image" : await giveImage(1)}

# # async def giveImage(num):
# #     file_path = f"/home/ubuntu/work/images/{num}/당근_양념겉절이_1.png"
    
# #     with open("/home/ubuntu/work/images/1/당근_양념겉절이_1.png", "rb") as image_file:
# #         encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
# #     return JSONResponse(content={"image_base64": encoded_string})

#     # if not os.path.exists(file_path):
#     #     print(file_path)
#     #     return {"error": "파일이 존재하지 않음"}
#     # return FileResponse(file_path, media_type="png")

# @app.post("/MakeImage/")
# async def createImage(FormakeImage: List[ForMakeImage]):

#     print(FormakeImage)
    
#     # for item in ForMakeImage:
#     #     item.kimchi_num, item.kimchi_name, item.recipe_order, item.recipe_detail
    
#     # print(FormakeImage)

#     list_of_prompts = []
    
#     for row in FormakeImage:
#         recipe_name = row.kimchi_name
#         step = row.recipe_order
#         recipe_detail = row.recipe_detail
        
#         prompts = full_recipe_to_image_prompts(recipe_detail, input_type="text")
#         list_of_prompts.append((recipe_name, prompts))
        
#     print(list_of_prompts)
    
    
#     # for recipe_name, pmts in list_of_prompts:
        
#     #     subprocess.run([
#     #         "python3", "model/stable-diffusion-xl-base-1.0.py",
#     #         json.dumps({
#     #             "name": recipe_name,
#     #             "prompts": pmts
#     #         })
#     #     ])
    

# @app.post("/MakeImage2/")
# async def createImage2(FormakeImage: List[ForMakeImage]):
#     i = 1
#     for row in FormakeImage:
#         recipe_name = row.kimchi_name
#         raw_step_data = row.recipe_detail  # list or image

#         input_type = detect_input_type(raw_step_data)
        
#         print(f"\n📌 Processing: {recipe_name} ({i}) [{input_type}]")
#         print(raw_step_data)

#         #여기까지는 잘 되는데

#         try:
#             prompts = full_recipe_to_image_prompts(raw_step_data, input_type=input_type)
        
#             #여기서 prompts를 저장할 때 1[1,2,3] 2[1,2,3] 3[1,2,3] 이런 방식으로 저장됨
    
#             # subprocess.run([
#             #     "python3", "model/stable-diffusion-xl-base-1.0.py",
#             #     json.dumps({
#             #         "name": recipe_name,
#             #         "prompts": raw_step_data
#             #         })
#             # ])
            
#             # for i, p in enumerate(prompts, 1):
#             #     print(f"🖼️ Step {i}:", p)

#             # subprocess.run([
#             #     "python3", "model/stable-diffusion-xl-base-1.0.py",
#             #     json.dumps({
#             #         "name": recipe_name,
#             #         "prompts": prompts
#             #         })
#             #         ]) 
            
#         # except Exception as e:
#             # print(f"❌ Error processing '{recipe_name}' at index {idx}: {e}")
        
#         i += 1




# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# from fastapi.responses import JSONResponse
# import subprocess
# import json

# from ocr_utils import extract_text_from_image
# from step_parser import parse_steps_with_llm
# from prompt_generator import generate_image_prompts_from_steps
# from main import full_recipe_to_image_prompts, detect_input_type

# app = FastAPI()

# class ForMakeImage(BaseModel):
#     kimchi_num: int
#     kimchi_name: str
#     recipe_order: int
#     recipe_detail: str

# @app.get("/")
# def root():
#     return {"message": "Hello, Kimchi Image API!"}

# @app.post("/MakeImage/")
# async def make_image_endpoint(FormakeImage: List[ForMakeImage]):
#     kimchi_dict = {}

#     # 🔸 Step 1: 김치 번호별로 그룹화
#     for row in FormakeImage:
#         key = (row.kimchi_num, row.kimchi_name)
#         kimchi_dict.setdefault(key, []).append((row.recipe_order, row.recipe_detail))

#     response_log = []

#     # 🔸 Step 2: 그룹별로 처리
#     for (kimchi_num, recipe_name), steps in kimchi_dict.items():
#         sorted_steps = [s for _, s in sorted(steps, key=lambda x: x[0])]
#         full_text = "\n".join(sorted_steps)

#         try:
#             input_type = detect_input_type(full_text)
#             prompts = full_recipe_to_image_prompts(full_text, input_type=input_type)

#             subprocess.run([
#                 "python3", "model/stable-diffusion-xl-base-1.0.py",
#                 json.dumps({
#                     "name": recipe_name,
#                     "prompts": prompts
#                 })
#             ])

#             response_log.append({
#                 "kimchi_num": kimchi_num,
#                 "kimchi_name": recipe_name,
#                 "num_prompts": len(prompts),
#                 "status": "✅ Success"
#             })
            
#             giveImage(kimchi_num)

#         except Exception as e:
#             response_log.append({
#                 "kimchi_num": kimchi_num,
#                 "kimchi_name": recipe_name,
#                 "status": f"❌ Error: {str(e)}"
#             })

#     return JSONResponse(content={"results": response_log})

# async def giveImage(num):
#     file_path = f"/home/ubuntu/work/images/{num}/당근_양념겉절이_1.png"
    
#     with open(f"/home/ubuntu/work/images/{num}/당근_양념겉절이_1.png", "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
#     return JSONResponse(content={"image_base64": encoded_string})

#     if not os.path.exists(file_path):
#         print(file_path)
#         return {"error": "파일이 존재하지 않음"}
#     return FileResponse(file_path, media_type="png")

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import subprocess
import json
import os
import base64
import re

from ocr_utils import extract_text_from_image
from step_parser import parse_steps_with_llm
from prompt_generator import generate_image_prompts_from_steps
from main2 import full_recipe_to_image_prompts, detect_input_type

app = FastAPI()

class ForMakeImage(BaseModel):
    kimchi_num: int
    kimchi_name: str
    recipe_order: int
    recipe_detail: str

@app.get("/")
def root():
    return {"message": "Hello, Kimchi Image API!"}


@app.post("/MakeImage/")
async def make_image_endpoint(FormakeImage: List[ForMakeImage]):
    kimchi_dict = {}
    response_log = []

    print("startMadeImage")

    # 🔸 Step 1: 김치 번호별로 그룹화
    for row in FormakeImage:
        key = (row.kimchi_num, row.kimchi_name)
        kimchi_dict.setdefault(key, []).append((row.recipe_order, row.recipe_detail))

    # 🔸 Step 2: 그룹별로 처리
    for (kimchi_num, recipe_name), steps in kimchi_dict.items():
        sorted_steps = [s for _, s in sorted(steps, key=lambda x: x[0])]
        full_text = "\n".join(sorted_steps)

        print(steps)

        try:
            input_type = detect_input_type(full_text)
            prompts = full_recipe_to_image_prompts(full_text, input_type=input_type)

            subprocess.run([
                "python3", "model/stable-diffusion-xl-base-1.0.py",
                # "python3", "model/stable-diffusion-xl-base-1.0.py",
                json.dumps({
                    "name": recipe_name,
                    "prompts": prompts
                })
            ])

            # 🔸 Step 3: 이미지 base64 포함
            image_payload = await giveImage(kimchi_num)

            response_log.append({
                "kimchi_num": kimchi_num,
                "kimchi_name": recipe_name,
                "num_prompts": len(prompts),
                "steps": steps,
                "status": "✅ Success",
                "prompts": prompts,
                "images": image_payload["images"]
            })

        except Exception as e:
            response_log.append({
                "kimchi_num": kimchi_num,
                "kimchi_name": recipe_name,
                "status": f"❌ Error: {str(e)}"
            })

    return JSONResponse(content={"results": response_log})


# ✅ 여러 이미지 정규식 기반으로 읽어서 base64로 리턴
async def giveImage(num: int):
    image_dir = f"/home/ubuntu/work/images/{num}/"
    pattern = re.compile(r'^.+_(\d+)\.png$')

    if not os.path.exists(image_dir):
        return {"images": []}

    images = []

    for filename in sorted(os.listdir(image_dir)):
        if pattern.match(filename):
            path = os.path.join(image_dir, filename)
            with open(path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode("utf-8")
                images.append({
                    "filename": filename,
                    "image_base64": encoded
                })

    return {"images": images}



@app.get("/sortExample")
async def sortExample():
    return await giveImage(1)