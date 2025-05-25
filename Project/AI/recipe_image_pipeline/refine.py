from langchain.chains import LLMChain
from .config import LLM_STAGE0
from .marker import add_markers
from .vectorstore import load_chroma
from .prompt_templates import REFINE_TEMPLATE

_retriever = load_chroma().as_retriever(search_type="similarity", search_kwargs={"k": 3})


def refine_recipe(text: str) -> str:
    marked = add_markers(text)
    ctx = "\n".join("• " + d.page_content for d in _retriever.get_relevant_documents(text[:500]))
    return LLMChain(llm=LLM_STAGE0, prompt=REFINE_TEMPLATE).run(recipe_marked=marked, context=ctx).strip()