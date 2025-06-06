import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io

def parse_uploaded_file(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
    else:
        image = Image.open(file)
        text = pytesseract.image_to_string(image, lang='chi_sim')
    return text