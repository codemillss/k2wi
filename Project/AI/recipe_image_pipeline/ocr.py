from PIL import Image
import pytesseract

def extract_text(img: Image.Image) -> str:
    text = pytesseract.image_to_string(img, lang="kor+eng").strip()
    if not text:
        raise ValueError("이미지에서 텍스트를 추출할 수 없습니다.")
    return text