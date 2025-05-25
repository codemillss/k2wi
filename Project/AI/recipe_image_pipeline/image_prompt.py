from langchain.chains import LLMChain
from .config import LLM_STAGE2
from .prompt_templates import SD_TEMPLATE
from .visual_sub import apply

_chain = LLMChain(llm=LLM_STAGE2, prompt=SD_TEMPLATE)

def generate(step_ko: str) -> str:
    return _chain.run(step_kor=apply(step_ko)).strip()