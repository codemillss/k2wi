from PIL import Image
import pytesseract

def extract_text_from_image(image: Image.Image) -> str:
    ocr_text = pytesseract.image_to_string(image, lang="kor+eng")
    if not ocr_text.strip():
        raise ValueError("이미지에서 텍스트를 추출할 수 없습니다.")
    return ocr_text.strip()