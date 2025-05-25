import re

_PATTERN = re.compile(r"★\d+★\s*(.*?)(?=★\d+★|$)", flags=re.S)

def parse_steps(text: str):
    steps = _PATTERN.findall(text)
    if not steps:
        raise ValueError("마커 분리 실패 – Stage‑0 출력 확인")
    return [s.strip() for s in steps]