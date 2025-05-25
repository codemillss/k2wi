from langchain.prompts import PromptTemplate

# —— Stage‑0 template (few‑shot) ——
REFINE_TEMPLATE = PromptTemplate.from_template(
"""
[RECIPE]
{recipe_marked}

[CONTEXT]
{context}

[TASK]
★1★, ★2★ … 마커와 번호를 절대 삭제·합치지 말고, 한 문장으로 보강하라.
모호한 ‘양념’ 대신 구체적 재료를 나열하라.
불필요한 조리 동작은 추가하지 마라.

출력:
"""
)


# —— Stage‑2 template ——
SD_TEMPLATE = PromptTemplate.from_template(
"""
Rewrite the Korean cooking step below as ONE concise English sentence for image generation.

Follow these rules:
• Start with action+tool+main ingredient(s).
• Use VISUAL_SUB names exactly.
• End with: at a 45-degree angle, on a wooden kitchen table, warm natural light, gloved hands, traditional Korean kitchen, vibrant food colors, photo-realistic, high detail, soft shadows, depth of field.
• Return the sentence ONLY.

Korean: {step_kor}
English:
"""
)
