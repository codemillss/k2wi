import re

_MARKER_PATTERN = re.compile(r"^\s*(\d+)\.\s*", flags=re.M)

def add_markers(text: str) -> str:
    return _MARKER_PATTERN.sub(lambda m: f"★{m.group(1)}★ ", text)