from pathlib import Path
from PIL import Image
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from docx import Document as DocxDocument

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def extract_text_from_image(file_path: str) -> str:
    try:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image, lang="fra+eng")
    except Exception as e:
        print(f"Erreur OCR sur l'image '{file_path}': {e}")
        return ""


def extract_text_from_pdf(file_path: str, ocr_threshold: int = 150) -> str:
    text_pages = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page_text := page.extract_text():
                    text_pages.append(page_text)
    except Exception as e:
        print(f"Erreur lors de l'ouverture du PDF '{file_path}': {e}")
        return ""

    text = "\n".join(text_pages)

    if len(text.strip()) < ocr_threshold:
        print(f"Texte court ({len(text.strip())} car.) — bascule OCR pour '{file_path}'")
        return _extract_text_with_ocr(file_path)

    return text


def _extract_text_with_ocr(file_path: str) -> str:
    try:
        pages = convert_from_path(file_path)
        ocr_pages = []
        for page_image in pages:
            try:
                ocr_pages.append(pytesseract.image_to_string(page_image, lang="fra+eng"))
            except Exception as e:
                print(f"Erreur OCR sur une page: {e}")
        return "\n".join(ocr_pages)
    except Exception as e:
        print(f"Erreur conversion PDF->image: {e}")
        return ""


def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = DocxDocument(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        print(f"Erreur lors de l'ouverture du DOCX '{file_path}': {e}")
        return ""


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        print(f"Fichier introuvable: {file_path}")
        return ""

    ext = path.suffix.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    if ext == ".docx":
        return extract_text_from_docx(file_path)
    if ext in IMAGE_EXTENSIONS:
        return extract_text_from_image(file_path)

    print(f"Format non supporté: {ext}")
    return ""