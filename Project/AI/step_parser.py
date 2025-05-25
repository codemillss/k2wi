import re
from typing import List
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

llm = Ollama(model="gemma3:12b") #12b로 바꿀것

parse_prompt = PromptTemplate.from_template(
    """
다음 요리 설명을 조리 단계별로 1, 2, 3, ... 형식으로 나누어 주세요.  
각 단계는 **간결하고 구체적으로** 작성하되, 다음 지침을 반드시 따르세요:

1. 각 단계는 **주어 + 조리 동작 + 식재료 + 조리도구**가 포함된 완전한 문장으로 표현합니다.  
2. 만약 주어나 재료가 생략되었거나 모호하다면, **이전 단계의 흐름과 재료를 참조하여 추론한 내용을 명시적으로 작성**하세요.  
    - 실제 텍스트에 등장하지 않은 **불필요한 조리 동작(blanching, boiling 등)은 추론하지 마세요.**
    - 이전 단계에서 이미 수행한 동작(예: 같은 재료를 반복 써는 것 등)은 **중복하지 마세요.**
3. 각 단계는 가능한 한 **시각적으로 그릴 수 있을 정도로 구체적인 동작 중심**으로 설명합니다.

요리 설명:
'''{content}'''

단계:
"""
)

def parse_steps_with_llm(raw_input: str) -> List[str]:
    chain = LLMChain(llm=llm, prompt=parse_prompt)
    parsed = chain.run(content=raw_input).strip()
    steps = re.findall(r'\d+\.\s+(.*?)(?=\d+\.\s+|$)', parsed, re.DOTALL)
    return [s.strip() for s in steps] if steps else [s.strip() for s in parsed.split("\n") if s.strip()]
