from pypdf import PdfReader  # type: ignore
from docx import Document  # type: ignore

def extract_requirements(file_path):

    if file_path.suffix.lower() == ".pdf":

        reader = PdfReader(str(file_path))

        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    elif file_path.suffix.lower() == ".docx":

        doc = Document(str(file_path))

        text = "\n".join(
            para.text
            for para in doc.paragraphs
        )

        return text

    elif file_path.suffix.lower() == ".txt":

        return file_path.read_text(
            encoding="utf-8"
        )

    return ""