import re
from typing import List
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

llm = Ollama(model="gemma3:4b") #12b로 바꿀것

VISUAL_SUBSTITUTE_DICT = {
    "쪽파": "scallions",
    "청갓": "mustard greens",
    "고들빼기": "wild lettuce",
    "까나리액젓": "fish sauce",
    "물엿": "starch syrup",
    "찹쌀풀": "rice paste",
    "고운 고춧가루": "chili flakes",
    "마늘": "garlic",
    "통깨": "sesame seeds",
    "당근": "carrots"
}

image_prompt_template = PromptTemplate.from_template(
    """
[입력: 조리 단계 (한국어)]
{content}

[Stable Diffusion Prompt 생성 규칙]

1. 문장을 자연스럽고 간결한 영어로 번역합니다.
2. 재료명은 시각적으로 표현 가능한 영어 단어로 자동 치환합니다. (예: 쪽파 → scallions)
3. **조리 동작 + 도구 + 핵심 재료**를 문장 앞부분에 배치하여 CLIP 모델이 시각적으로 강조할 수 있도록 합니다.
4. 도구는 가능한 구체적으로 표현합니다. (예: 칼 → kitchen knife, 절구 → stone mortar and pestle, 채칼 → vegetable slicer 등)
5. 아래 고정된 배경 및 스타일 문구를 문장 끝에 추가하세요:

    at 45-degree angle, on wooden kitchen table, warm natural light, gloved hands, traditional Korean kitchen, vibrant food colors, photo-realistic, high detail, soft shadows, depth of field

[출력 형식]
→ Prompt: [번역된 문장] at a 45-degree angle, on a wooden kitchen table, warm natural light, gloved hands, traditional Korean kitchen, vibrant food colors, photo-realistic, high detail, soft shadows, depth of field
"""
)

def apply_visual_substitution(text: str) -> str:
    for kor, eng in VISUAL_SUBSTITUTE_DICT.items():
        text = text.replace(kor, eng)
    return text

def generate_image_prompts_from_steps(steps: List[str]) -> List[str]:
    chain = LLMChain(llm=llm, prompt=image_prompt_template)
    prompts = []

    for step in steps:
        step = apply_visual_substitution(step)
        result = chain.run(content=step).strip()
        prompt = re.search(r'→ Prompt: (.*)', result)
        final_prompt = prompt.group(1) if prompt else result
        prompts.append(final_prompt)

    return prompts
