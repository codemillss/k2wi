VISUAL_SUB = {
    "쪽파": "scallions",  "청갓": "mustard greens", "고들빼기": "wild lettuce",
    "까나리액젓": "fish sauce", "물엿": "starch syrup", "찹쌀풀": "rice paste",
    "고운 고춧가루": "fine chili flakes", "고춧가루": "red chili flakes",
    "마늘": "garlic", "통깨": "sesame seeds", "당근": "carrots",
    "간장": "soy sauce", "배추": "napa cabbage", "김치": "kimchi",
}

def apply(text: str) -> str:
    for k, v in VISUAL_SUB.items():
        text = text.replace(k, v)
    return text