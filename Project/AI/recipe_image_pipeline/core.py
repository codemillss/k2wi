from typing import Union, Sequence, List
from PIL import Image
from .ocr import extract_text
from .refine import refine_recipe
from .step_parser import parse_steps
from .image_prompt import generate
from .visual_sub import apply          # ← 존재해야 함
apply_visual_substitution = apply

__all__ = [
    "recipe_to_image_prompts",
    "full_recipe_to_image_prompts",
    "parse_steps_with_llm",
    "apply_visual_substitution",
    "generate_image_prompts_from_steps",
]

def recipe_to_image_prompts(data: Union[str, Image.Image, Sequence[str]]) -> List[str]:
    if isinstance(data, (list, tuple)):
        raw = "\n".join(map(str, data))
    elif isinstance(data, Image.Image):
        raw = extract_text(data)
    else:
        raw = str(data).strip()

    refined = refine_recipe(raw)
    steps = parse_steps(refined)
    return [generate(s) for s in steps]

# backwards compatibility wrappers
full_recipe_to_image_prompts = recipe_to_image_prompts
parse_steps_with_llm = lambda txt: parse_steps(refine_recipe(txt))
apply_visual_substitution = apply  # from visual_sub
generate_image_prompts_from_steps = lambda steps: [generate(s) for s in steps]