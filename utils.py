import PyPDF2
import io


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF file (Streamlit UploadedFile object)."""
    try:
        pdf_bytes = uploaded_file.read()
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_score(text: str, pattern: str = "Score:") -> str:
    """Pull score value from agent output for display."""
    for line in text.split("\n"):
        if pattern.lower() in line.lower():
            parts = line.split(":")
            if len(parts) > 1:
                return parts[1].strip().split()[0].replace("*", "")
    return "—"
